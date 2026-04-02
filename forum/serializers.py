from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Post, Reply, Like, Favorite


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']


class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'post_count', 'order']


class ReplySerializer(serializers.ModelSerializer):
    """回复序列化器"""
    
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    
    class Meta:
        model = Reply
        fields = [
            'id', 'content', 'author', 'author_username', 'author_id',
            'parent', 'floor', 'like_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['author', 'floor']


class PostSerializer(serializers.ModelSerializer):
    """帖子序列化器"""
    
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    reply_count = serializers.IntegerField(read_only=True)
    view_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author', 'author_username', 'author_id',
            'category', 'category_name', 'is_pinned', 'is_locked',
            'view_count', 'reply_count', 'like_count',
            'created_at', 'updated_at', 'last_reply_at'
        ]
        read_only_fields = ['author', 'view_count', 'reply_count', 'like_count']


class PostDetailSerializer(PostSerializer):
    """帖子详情序列化器（包含更多关联信息）"""
    replies = ReplySerializer(many=True, read_only=True)
    
    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['replies']


class LikeSerializer(serializers.ModelSerializer):
    """点赞序列化器"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'user_username', 'content_type', 'object_id', 'created_at']
        read_only_fields = ['user']


class FavoriteSerializer(serializers.ModelSerializer):
    """收藏序列化器"""
    
    post_title = serializers.CharField(source='post.title', read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'post', 'post_title', 'created_at']
        read_only_fields = ['user']