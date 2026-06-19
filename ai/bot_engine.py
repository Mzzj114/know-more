"""
论坛机器人行动引擎
使用 OpenAI API + Tool Calling 实现智能论坛互动
"""
import os
import json
import logging
from openai import OpenAI
from django.contrib.auth.models import User
from django.utils import timezone
from .models import BotProfile, BotActionLog
from .forum_tools import (
    exit_bot, add_to_favourite, like, reply, post, 
    read_post, get_forum_overview
)

logger = logging.getLogger(__name__)


# 工具 Schema 定义
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "exit_bot",
            "description": "机器人下线，结束今天的活动。当完成所有任务或决定停止时使用。",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_to_favourite",
            "description": "收藏感兴趣的帖子",
            "parameters": {
                "type": "object",
                "properties": {
                    "post_id": {"type": "integer", "description": "要收藏的帖子ID"}
                },
                "required": ["post_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "like",
            "description": "点赞帖子或回复",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_type": {
                        "type": "integer",
                        "description": "目标类型：1=帖子，2=回复",
                        "enum": [1, 2]
                    },
                    "target_id": {"type": "integer", "description": "目标ID（帖子ID或回复ID）"}
                },
                "required": ["target_type", "target_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reply",
            "description": "回复帖子或其他用户的回复",
            "parameters": {
                "type": "object",
                "properties": {
                    "post_id": {"type": "integer", "description": "要回复的帖子ID"},
                    "content": {"type": "string", "description": "回复的内容"},
                    "parent_reply_id": {
                        "type": "integer",
                        "description": "父回复ID（可选，如果回复的是某个特定回复而不是帖子本身）"
                    }
                },
                "required": ["post_id", "content"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "post",
            "description": "发布新帖子",
            "parameters": {
                "type": "object",
                "properties": {
                    "category_id": {"type": "integer", "description": "分类ID"},
                    "title": {"type": "string", "description": "帖子标题"},
                    "content": {"type": "string", "description": "帖子内容"}
                },
                "required": ["category_id", "title", "content"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_post",
            "description": "读取帖子的详细信息和回复内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "post_id": {"type": "integer", "description": "要阅读的帖子ID"}
                },
                "required": ["post_id"],
                "additionalProperties": False
            }
        }
    }
]

# 工具函数映射表
TOOL_DISPATCH = {
    "exit_bot": exit_bot,
    "add_to_favourite": add_to_favourite,
    "like": like,
    "reply": reply,
    "post": post,
    "read_post": read_post,
}


def execute_bot_action(bot_user_id):
    """
    执行机器人行动的主函数
    由 django-q2 异步调用
    
    Args:
        bot_user_id: 机器人绑定的用户ID
    """
    try:
        bot_user = User.objects.get(id=bot_user_id)
        bot_profile = BotProfile.objects.get(user=bot_user)
        
        if not bot_profile.is_active:
            logger.info(f"机器人 {bot_profile.name} 未激活，跳过执行")
            return f"机器人 {bot_profile.name} 未激活，跳过执行"
        
        logger.info(f"开始执行机器人: {bot_profile.name}")
        
        # 获取论坛概览
        forum_data = get_forum_overview()
        
        # 构建系统提示词
        system_prompt = f"""
{bot_profile.persona_prompt}

{bot_profile.workflow_prompt}

## 当前论坛状态
分区列表：
{json.dumps(forum_data['sections'], ensure_ascii=False, indent=2)}

各分区首页帖子：
{json.dumps(forum_data['posts_overview'], ensure_ascii=False, indent=2)}

请开始你的论坛活动吧！记住使用工具来执行操作。
"""
        
        # 初始化消息历史
        input_messages = [
            {"role": "system", "content": system_prompt},
        ]
        
        # 获取 OpenAI 客户端（复用 ai app 的配置）
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            raise Exception("未配置 OPENAI_API_KEY 环境变量")
        
        client = OpenAI(api_key=api_key)
        
        # 多轮工具调用循环
        max_iterations = 20  # 防止无限循环
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # 调用模型
            response = client.chat.completions.create(
                model="deepseek-chat",  # 可根据需要调整模型
                messages=input_messages,
                tools=TOOLS
            )
            
            message = response.choices[0].message
            
            # 检查是否有工具调用
            if not message.tool_calls:
                # 没有工具调用，记录并结束
                logger.info(f"AI 回复: {message.content}")
                break
            
            # 添加助手响应到消息历史
            input_messages.append(message)
            
            # 处理所有工具调用
            for tool_call in message.tool_calls:
                args = json.loads(tool_call.function.arguments)
                name = tool_call.function.name
                
                logger.info(f"工具调用: {name}, 参数: {args}")
                
                # 记录行动日志
                log_entry = BotActionLog.objects.create(
                    bot=bot_profile,
                    action_type=_map_tool_to_action_type(name),
                    target_id=args.get('post_id') or args.get('target_id'),
                    content_preview=str(args.get('content', ''))[:200],
                    ai_prompt_used=json.dumps(input_messages[-3:], ensure_ascii=False)[:1000] if len(input_messages) >= 3 else '',
                    ai_response=message.content or '',
                    status='pending',
                    scheduled_at=bot_profile.last_action_at or bot_profile.created_at,
                )
                
                # 使用字典映射调用对应函数
                try:
                    if name in TOOL_DISPATCH:
                        # 对于需要 bot_user 的工具，注入用户参数
                        if name in ['exit_bot', 'add_to_favourite', 'like', 'reply', 'post']:
                            result = TOOL_DISPATCH[name](bot_user, **args)
                        else:
                            result = TOOL_DISPATCH[name](**args)
                    else:
                        result = f"未知工具: {name}"
                    
                    logger.info(f"工具结果: {result}")
                    
                    # 更新日志状态
                    log_entry.status = 'success'
                    log_entry.executed_at = timezone.now()
                    log_entry.save()
                    
                    # 添加工具结果到消息历史
                    input_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": name,
                        "content": str(result)
                    })
                    
                    # 如果是 exit_bot，结束循环
                    if name == 'exit_bot':
                        bot_profile.last_action_at = timezone.now()
                        bot_profile.save(update_fields=['last_action_at'])
                        return result
                    
                except Exception as e:
                    error_msg = f"工具执行错误: {str(e)}"
                    logger.error(f"错误: {error_msg}", exc_info=True)
                    
                    # 更新日志状态
                    log_entry.status = 'failed'
                    log_entry.error_message = error_msg
                    log_entry.executed_at = timezone.now()
                    log_entry.save()
                    
                    input_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": name,
                        "content": error_msg
                    })
        
        # 更新最后行动时间
        bot_profile.last_action_at = timezone.now()
        bot_profile.save(update_fields=['last_action_at'])
        
        return f"机器人 {bot_profile.name} 完成本轮行动"
        
    except Exception as e:
        logger.error(f"执行失败: {str(e)}", exc_info=True)
        raise


def _map_tool_to_action_type(tool_name):
    """将工具名称映射为行动类型"""
    mapping = {
        'exit_bot': 'read',
        'add_to_favourite': 'favorite',
        'like': 'like_post',  # 简化处理，实际应根据参数判断
        'reply': 'reply',
        'post': 'post',
        'read_post': 'read',
    }
    return mapping.get(tool_name, 'read')
