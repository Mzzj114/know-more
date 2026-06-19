"""
论坛机器人工具函数
提供 AI 可调用的论坛操作接口
"""
from django.contrib.auth.models import User
from forum.models import Category, Post, Reply, Like, Favorite
from forum.services import PostService, ReplyService, InteractionService
from django.contrib.contenttypes.models import ContentType


def exit_bot(bot_user):
    """机器人下线，结束今天的活动"""
    from ai.models import BotProfile
    bot_profile = BotProfile.objects.get(user=bot_user)
    return f"机器人 {bot_profile.name} 已下线，结束今天的活动"


def add_to_favourite(bot_user, post_id):
    """收藏帖子"""
    try:
        post = Post.objects.get(id=post_id, is_hidden=False)
        favorited = InteractionService.toggle_favorite(bot_user, post)
        if favorited:
            return f"已成功收藏帖子 {post_id}: {post.title}"
        else:
            return f"已取消收藏帖子 {post_id}"
    except Post.DoesNotExist:
        return f"帖子 {post_id} 不存在"
    except Exception as e:
        return f"收藏失败: {str(e)}"


def like(bot_user, target_type, target_id):
    """点赞帖子或回复
    target_type: 1=帖子, 2=回复
    target_id: 目标ID
    """
    try:
        if target_type == 1:
            obj = Post.objects.get(id=target_id, is_hidden=False)
            obj_type = "帖子"
        elif target_type == 2:
            obj = Reply.objects.get(id=target_id, is_hidden=False)
            obj_type = "回复"
        else:
            return f"无效的目标类型: {target_type}"
        
        liked, updated_obj = InteractionService.toggle_like(bot_user, obj)
        if liked:
            return f"已点赞{obj_type} {target_id}"
        else:
            return f"已取消点赞{obj_type} {target_id}"
    except (Post.DoesNotExist, Reply.DoesNotExist):
        return f"{obj_type} {target_id} 不存在"
    except Exception as e:
        return f"点赞失败: {str(e)}"


def reply(bot_user, post_id, content, parent_reply_id=None):
    """回复帖子或回复
    post_id: 帖子ID
    parent_reply_id: 父回复ID（可选）
    content: 回复内容
    """
    try:
        post = Post.objects.get(id=post_id, is_hidden=False)
        parent = None
        if parent_reply_id:
            parent = Reply.objects.get(id=parent_reply_id)
        
        reply_obj = ReplyService.create_reply(
            author=bot_user,
            post=post,
            content=content,
            parent=parent
        )
        
        if parent:
            return f"已回复帖子 {post_id} 的回复 {parent_reply_id}"
        else:
            return f"已回复帖子 {post_id}"
    except Post.DoesNotExist:
        return f"帖子 {post_id} 不存在"
    except Reply.DoesNotExist:
        return f"回复 {parent_reply_id} 不存在"
    except Exception as e:
        return f"回复失败: {str(e)}"


def post(bot_user, category_id, title, content):
    """发帖
    category_id: 分类ID
    title: 标题
    content: 内容
    """
    try:
        post_obj = PostService.create_post(
            author=bot_user,
            title=title,
            content=content,
            category_id=category_id
        )
        return f"已在分类 {category_id} 发布帖子: {title}"
    except Category.DoesNotExist:
        return f"分类 {category_id} 不存在"
    except Exception as e:
        return f"发帖失败: {str(e)}"


def read_post(post_id):
    """读取帖子详情和回复
    post_id: 帖子ID
    """
    try:
        post = Post.objects.select_related('author').get(id=post_id, is_hidden=False)
        replies = post.replies.filter(is_hidden=False).order_by('created_at')[:10]  # 最多返回10条回复
        
        result = f"帖子标题: {post.title}\n作者: {post.author.username}\n内容: {post.content[:200]}...\n"
        
        if replies:
            result += f"\n回复({len(replies)}条):\n"
            for r in replies:
                result += f"- [{r.id}] {r.author.username}: {r.content[:100]}\n"
        else:
            result += "\n暂无回复"
        
        return result
    except Post.DoesNotExist:
        return f"未找到帖子 {post_id}"
    except Exception as e:
        return f"读取失败: {str(e)}"


def get_forum_overview():
    """获取论坛概览信息（分区、帖子列表）"""
    categories = Category.objects.filter(is_active=True).order_by('order')
    
    sections = []
    posts_overview = {}
    
    for cat in categories:
        sections.append({
            'id': str(cat.id),
            'name': cat.name
        })
        
        # 获取该分类下的最新帖子（最多5个）
        posts = Post.objects.filter(
            category=cat,
            is_hidden=False
        ).order_by('-is_pinned', '-last_reply_at', '-created_at')[:5]
        
        posts_overview[str(cat.id)] = [
            {'id': str(p.id), 'title': p.title}
            for p in posts
        ]
    
    return {
        'sections': sections,
        'posts_overview': posts_overview
    }
