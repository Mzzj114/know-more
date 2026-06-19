from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserTokenUsage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ai_token_usage', verbose_name='用户')
    remaining_tokens = models.IntegerField(default=50000, verbose_name='剩余可用 Tokens')
    last_reset_date = models.DateField(default=timezone.now, verbose_name='上次重置日期')

    class Meta:
        verbose_name = '用户 Token 使用量'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user.username} 的 Token 容量'


class BotProfile(models.Model):
    """机器人档案"""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='bot_profile',
        verbose_name='绑定用户'
    )
    
    # 人物设定
    name = models.CharField(max_length=50, verbose_name='机器人名称')
    persona_prompt = models.TextField(verbose_name='人物设定提示词')
    workflow_prompt = models.TextField(default='', verbose_name='工作流程提示词')
    
    # 行为配置
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    weekly_action_count = models.IntegerField(default=3, verbose_name='每周行动次数')
    
    # 统计信息
    total_posts = models.PositiveIntegerField(default=0, verbose_name='总发帖数')
    total_replies = models.PositiveIntegerField(default=0, verbose_name='总回复数')
    total_likes = models.PositiveIntegerField(default=0, verbose_name='总点赞数')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_action_at = models.DateTimeField(null=True, blank=True, verbose_name='最后行动时间')
    
    class Meta:
        verbose_name = '机器人档案'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f'{self.name} ({self.user.username})'


class BotActionLog(models.Model):
    """机器人行动日志"""
    bot = models.ForeignKey(
        BotProfile,
        on_delete=models.CASCADE,
        related_name='action_logs',
        verbose_name='机器人'
    )
    
    # 行动类型
    ACTION_TYPES = [
        ('post', '发帖'),
        ('reply', '回复'),
        ('like_post', '点赞帖子'),
        ('like_reply', '点赞回复'),
        ('favorite', '收藏'),
        ('read', '阅读'),
    ]
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES, verbose_name='行动类型')
    
    # 行动详情
    target_id = models.IntegerField(null=True, blank=True, verbose_name='目标ID')
    content_preview = models.TextField(blank=True, default='', verbose_name='内容预览')
    
    # AI 决策信息
    ai_prompt_used = models.TextField(blank=True, default='', verbose_name='使用的提示词')
    ai_response = models.TextField(blank=True, default='', verbose_name='AI响应')
    
    # 执行状态
    STATUS_CHOICES = [
        ('pending', '待执行'),
        ('success', '成功'),
        ('failed', '失败'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    error_message = models.TextField(blank=True, default='', verbose_name='错误信息')
    
    # 时间戳
    scheduled_at = models.DateTimeField(verbose_name='计划执行时间')
    executed_at = models.DateTimeField(null=True, blank=True, verbose_name='实际执行时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '机器人行动日志'
        verbose_name_plural = verbose_name
        ordering = ['-scheduled_at']
        indexes = [
            models.Index(fields=['bot', '-scheduled_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f'{self.bot.name} - {self.get_action_type_display()} at {self.scheduled_at}'
