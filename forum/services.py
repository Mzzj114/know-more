from django.utils import timezone
from django.db import transaction
from django.contrib.auth.models import User
from .models import Post, Reply, Category, Like, Favorite, UserProfile


class PostService:
    """帖子服务类"""
    
    @staticmethod
    def create_post(author, title, content, category_id):
        """创建帖子"""
        category = Category.objects.get(id=category_id)
        post = Post.objects.create(
            author=author,
            title=title,
            content=content,
            category=category,
        )
        
        # 更新分类统计
        category.post_count += 1
        category.last_post_time = timezone.now()
        category.save(update_fields=['post_count', 'last_post_time'])
        
        # 更新用户统计
        profile = author.profile
        profile.post_count += 1
        profile.save(update_fields=['post_count'])
        
        return post
    
    @staticmethod
    def update_post(post, title=None, content=None, category=None):
        """更新帖子"""
        if title:
            post.title = title
        if content:
            post.content = content
        if category:
            post.category = category
        
        post.save(update_fields=['title', 'content', 'category', 'updated_at'])
        return post
    
    @staticmethod
    @transaction.atomic
    def delete_post(post):
        """删除帖子"""
        # 更新分类统计
        category = post.category
        if category:
            category.post_count = max(0, category.post_count - 1)
            category.save(update_fields=['post_count'])
        
        # 更新作者统计
        author = post.author
        profile = author.profile
        profile.post_count = max(0, profile.post_count - 1)
        profile.save(update_fields=['post_count'])
        
        post.delete()
    
    @staticmethod
    def toggle_pin(post):
        """切换置顶状态"""
        post.is_pinned = not post.is_pinned
        post.save(update_fields=['is_pinned'])
        return post
    
    @staticmethod
    def toggle_lock(post):
        """切换锁定状态"""
        post.is_locked = not post.is_locked
        post.save(update_fields=['is_locked'])
        return post
    
    @staticmethod
    def increment_view_count(post):
        """增加浏览量"""
        post.view_count += 1
        post.save(update_fields=['view_count'])


class ReplyService:
    """回复服务类"""
    
    @staticmethod
    @transaction.atomic
    def create_reply(author, post, content, parent=None):
        """创建回复"""
        # 检查帖子是否被锁定
        if post.is_locked and parent is None:
            raise Exception('该帖子已被锁定，无法回复')
        
        reply = Reply.objects.create(
            author=author,
            post=post,
            content=content,
            parent=parent,
        )
        
        # 更新帖子统计
        post.update_reply_info()
        
        # 更新分类统计
        if post.category:
            post.category.last_post_time = timezone.now()
            post.category.save(update_fields=['last_post_time'])
        
        # 更新作者统计
        profile = author.profile
        profile.reply_count += 1
        profile.save(update_fields=['reply_count'])
        
        return reply
    
    @staticmethod
    @transaction.atomic
    def delete_reply(reply):
        """删除回复"""
        # 更新作者统计
        author = reply.author
        profile = author.profile
        profile.reply_count = max(0, profile.reply_count - 1)
        profile.save(update_fields=['reply_count'])
        
        post = reply.post
        reply.delete()
        
        # 更新帖子统计
        post.update_reply_info()


class InteractionService:
    """互动服务类（点赞、收藏）"""
    
    @staticmethod
    @transaction.atomic
    def toggle_like(user, obj):
        """切换点赞状态（支持帖子和回复）"""
        from django.contrib.contenttypes.models import ContentType
        
        existing_like = Like.objects.filter(
            user=user,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id
        ).first()
        
        if existing_like:
            # 取消点赞
            existing_like.delete()
            
            # 减少点赞数
            if isinstance(obj, Post):
                obj.like_count = max(0, obj.like_count - 1)
                obj.save(update_fields=['like_count'])
            elif isinstance(obj, Reply):
                obj.like_count = max(0, obj.like_count - 1)
                obj.save(update_fields=['like_count'])
            
            return False, obj  # 已取消
        else:
            # 添加点赞
            Like.objects.create(
                user=user,
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id
            )
            
            # 增加点赞数
            if isinstance(obj, Post):
                obj.like_count += 1
                obj.save(update_fields=['like_count'])
                
                # 更新被点赞用户的获赞数
                obj_author_profile = obj.author.profile
                obj_author_profile.like_count += 1
                obj_author_profile.save(update_fields=['like_count'])
                
            elif isinstance(obj, Reply):
                obj.like_count += 1
                obj.save(update_fields=['like_count'])
                
                # 更新被点赞用户的获赞数
                obj_author_profile = obj.author.profile
                obj_author_profile.like_count += 1
                obj_author_profile.save(update_fields=['like_count'])
            
            return True, obj  # 已点赞
    
    @staticmethod
    @transaction.atomic
    def toggle_favorite(user, post):
        """切换收藏状态"""
        existing_favorite = Favorite.objects.filter(
            user=user,
            post=post
        ).first()
        
        if existing_favorite:
            # 取消收藏
            existing_favorite.delete()
            post.favorite_count = max(0, post.favorite_count - 1)
            post.save(update_fields=['favorite_count'])
            return False  # 已取消
        else:
            # 添加收藏
            Favorite.objects.create(user=user, post=post)
            post.favorite_count += 1
            post.save(update_fields=['favorite_count'])
            return True  # 已收藏
    
    @staticmethod
    def get_user_favorites(user):
        """获取用户的收藏列表"""
        return Favorite.objects.filter(user=user).select_related('post').order_by('-created_at')