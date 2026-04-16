# 互动式教程文件清单

本目录包含 Know More 项目的互动式教程 JSON 文件，用于驱动前端教程页面。

## 已完成教程

### 1. 大语言模型与AI应用 (ai-and-prompt-engineering.json)
**Slug:** `ai-and-prompt-engineering`  
**步骤数:** 4步  
**内容概述:**
- 介绍大语言模型（LLM）的基本概念
- 区分大语言模型与AI应用的差异
- 说明本教程AI沙箱的功能和限制
- 引导用户进入下一个主题

**交互类型:** quiz, highlights, chat

---

### 2. 提示词工程 (prompt-engineering.json)
**Slug:** `prompt-engineering`  
**步骤数:** 5步  
**内容概述:**
- 定义提示词工程及其重要性
- 解释提示词工程的本质：清晰表达需求
- 展示"门槛低但上限高"的特点
- 通过对比示例展示好坏提示词的差异
- 预告后续学习内容

**交互类型:** quiz, chat

---

### 3. 明确任务与目标 (clear-goal.example.json)
**Slug:** `clear-goal`  
**步骤数:** 3步  
**内容概述:**
- 讲解明确任务与目标的重要性
- 通过量子纠缠科普文章的案例展示模糊指令的问题
- 测验：如何选择有效的限制条件
- 实践：填空练习完善提示词

**交互类型:** chat, highlights, quiz, fill_blank

---

### 4. 提供上下文背景 (provide-context.json)
**Slug:** `provide-context`  
**步骤数:** 6步  
**内容概述:**
- 解释为什么需要提供背景信息
- 对比缺少背景和包含背景的提问效果
- Django项目文件上传错误的实际案例
- 实践：为代码优化场景补充背景信息
- 总结背景信息的关键要素
- 预告下一个技巧

**交互类型:** quiz, chat, fill_blank

---

### 5. 使用示例引导 (few-shot-examples.json)
**Slug:** `few-shot-examples`  
**步骤数:** 7步  
**内容概述:**
- 介绍Few-shot Learning的概念和原理
- 语气转换任务的对比示例
- 实践：设计技术术语解释的示例
- 多示例的力量：代码注释风格案例
- 编写好示例的5个技巧
- 总结"提供信息的三大技巧"
- 预告下一个主题

**交互类型:** quiz, chat, fill_blank

---

## 教程结构规范

每个JSON文件遵循以下结构：

```json
{
    "title": "教程标题",
    "steps": [
        {
            "step": 1,
            "content": "Markdown格式的内容",
            "interaction": [
                {
                    "type": "chat|quiz|fill_blank|highlights",
                    // 根据类型有不同的字段
                }
            ]
        }
    ]
}
```

### 支持的交互类型

1. **chat** - 预设对话
   ```json
   {
       "type": "chat",
       "prompt": "发送给AI的消息"
   }
   ```

2. **quiz** - 知识测验
   ```json
   {
       "type": "quiz",
       "question": "问题文本",
       "options": ["选项A", "选项B", "选项C"],
       "correctIndex": 1,
       "explanation": "答案解析"
   }
   ```

3. **fill_blank** - 填空练习
   ```json
   {
       "type": "fill_blank",
       "template": "模板文本，使用{0}, {1}等占位符",
       "blanks": ["第一个空的提示", "第二个空的提示"]
   }
   ```

4. **highlights** - UI引导
   ```json
   {
       "type": "highlights",
       "selectors": [".css-selector"]
   }
   ```

---

## 待完成教程

根据`主要站需求.md`中的内容设计，还需完成以下教程：

- [x] 指示模型多视角回答 (multi-perspective-analysis.json)
- [x] 分步骤拆解逻辑 (chain-of-thought.json)
- [x] 精确控制输出形式 (control-output-format.json)
- [x] 元提示词 (meta-prompt.json)
- [x] 结构化提示词 (structured-prompt.json)
- [x] 对抗提示词 (adversarial-prompting.json)
- [ ] 案例：设计学习路线 (case-study-learning-path.json)

---

## 开发建议

1. **内容来源**: 参考 `document/zh/` 目录下的Markdown文档
2. **交互设计**: 每个教程应混合使用多种交互类型，增强学习体验
3. **教育哲学**: 交互的目的是增强体验，不限制用户的学习流程
4. **测试验证**: 创建JSON后，建议在浏览器中预览教程页面确保正常显示
