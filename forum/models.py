from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone


# ==================== 用户扩展模块 ====================

class UserProfile(models.Model):
    """
    用户个人资料 - 使用 OneToOne 关系扩展 Django 内置 User 模型
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name='用户'
    )
    
    # 个人信息
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/', 
        blank=True, 
        null=True,
        verbose_name='头像'
    )
    signature = models.CharField(
        max_length=255, 
        blank=True, 
        default='',
        verbose_name='个人签名'
    )
    bio = models.TextField(
        blank=True, 
        default='',
        verbose_name='个人简介'
    )
    
    # 统计信息
    post_count = models.PositiveIntegerField(default=0, verbose_name='发帖数')
    reply_count = models.PositiveIntegerField(default=0, verbose_name='回复数')
    like_count = models.PositiveIntegerField(default=0, verbose_name='获赞数')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f'{self.user.username} 的个人资料'


# ==================== 论坛核心模块 ====================

class Category(models.Model):
    """
    论坛分类/板块
    例如："提示词分享"、"学习路线案例"、"技术交流"等
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='分类名称')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL 标识')
    description = models.TextField(blank=True, default='', verbose_name='描述')
    
    # 排序和显示
    order = models.PositiveIntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    
    # 统计信息（冗余字段，提升性能）
    post_count = models.PositiveIntegerField(default=0, verbose_name='帖子数')
    last_post_time = models.DateTimeField(null=True, blank=True, verbose_name='最后发帖时间')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '论坛分类'
        verbose_name_plural = verbose_name
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.name


class Post(models.Model):
    """
    帖子/主题
    """
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')  # 支持 Markdown
    
    # 作者和分类
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='posts',
        verbose_name='作者'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='posts',
        verbose_name='分类'
    )
    
    # 状态标记
    is_pinned = models.BooleanField(default=False, verbose_name='置顶')
    is_locked = models.BooleanField(default=False, verbose_name='锁定')
    is_hidden = models.BooleanField(default=False, verbose_name='隐藏')
    
    # 统计信息（冗余字段）
    view_count = models.PositiveIntegerField(default=0, verbose_name='浏览量')
    reply_count = models.PositiveIntegerField(default=0, verbose_name='回复数')
    like_count = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    favorite_count = models.PositiveIntegerField(default=0, verbose_name='收藏数')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    last_reply_at = models.DateTimeField(null=True, blank=True, verbose_name='最后回复时间')
    
    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = verbose_name
        ordering = ['-is_pinned', '-last_reply_at', '-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['category', '-is_pinned', '-last_reply_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def increment_view_count(self):
        """增加浏览量"""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    def update_reply_info(self):
        """更新回复相关信息"""
        self.reply_count = self.replies.filter(is_hidden=False).count()
        self.last_reply_at = timezone.now()
        self.save(update_fields=['reply_count', 'last_reply_at'])
        
        # 同时更新分类的最后发帖时间
        if self.category:
            self.category.last_post_time = self.last_reply_at
            self.category.save(update_fields=['last_post_time'])


class Reply(models.Model):
    """
    回复/评论
    支持楼中楼（通过 parent 自引用）
    """
    content = models.TextField(verbose_name='内容')
    
    # 关联关系
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='replies',
        verbose_name='帖子'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='replies',
        verbose_name='作者'
    )
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='children',
        verbose_name='父回复'
    )
    
    # 楼层和信息
    floor = models.PositiveIntegerField(default=0, verbose_name='楼层')
    is_hidden = models.BooleanField(default=False, verbose_name='隐藏')
    like_count = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '回复'
        verbose_name_plural = verbose_name
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'created_at']),
        ]
    
    def __str__(self):
        return f'{self.author.username} 在 {self.post.title} 的回复'
    
    def save(self, *args, **kwargs):
        """保存时自动计算楼层"""
        if not self.floor:
            # 如果是楼中楼，不需要楼层号
            if self.parent:
                self.floor = 0
            else:
                # 主回复的楼层号
                max_floor = Reply.objects.filter(
                    post=self.post, 
                    parent__isnull=True
                ).aggregate(max_floor=models.Max('floor'))['max_floor']
                self.floor = (max_floor or 0) + 1
        
        super().save(*args, **kwargs)


# ==================== 互动模块 ====================

class Like(models.Model):
    """
    点赞记录
    可以点赞帖子或回复
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='likes',
        verbose_name='用户'
    )
    
    # 使用 GenericForeignKey 支持点赞不同对象
    content_type = models.ForeignKey(
        'contenttypes.ContentType', 
        on_delete=models.CASCADE,
        verbose_name='内容类型'
    )
    object_id = models.PositiveIntegerField(verbose_name='对象 ID')
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = verbose_name
        unique_together = ['user', 'content_type', 'object_id']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        return f'{self.user.username} 点赞了 {self.content_object}'


class Favorite(models.Model):
    """
    收藏记录
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='favorites',
        verbose_name='用户'
    )
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='favorited_by',
        verbose_name='帖子'
    )
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = verbose_name
        unique_together = ['user', 'post']
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} 收藏了 {self.post.title}'


# ==================== 标签模块（日后再说） ====================

# class Tag(models.Model):
#     """
#     标签
#     用于给帖子打标签，便于分类和搜索
#     """
#     name = models.CharField(max_length=50, unique=True, verbose_name='标签名')
#     slug = models.SlugField(max_length=50, unique=True, verbose_name='URL 标识')
#     usage_count = models.PositiveIntegerField(default=0, verbose_name='使用次数')
    
#     # 时间戳
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
#     class Meta:
#         verbose_name = '标签'
#         verbose_name_plural = verbose_name
    
#     def __str__(self):
#         return self.name


# class PostTag(models.Model):
#     """
#     帖子与标签的关联表（多对多关系的中间表）
#     """
#     post = models.ForeignKey(
#         Post, 
#         on_delete=models.CASCADE, 
#         related_name='tags',
#         verbose_name='帖子'
#     )
#     tag = models.ForeignKey(
#         Tag, 
#         on_delete=models.CASCADE, 
#         related_name='posts',
#         verbose_name='标签'
#     )
    
#     # 时间戳
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
#     class Meta:
#         verbose_name = '帖子标签'
#         verbose_name_plural = verbose_name
#         unique_together = ['post', 'tag']
    
#     def __str__(self):
#         return f'{self.post.title} - {self.tag.name}'
