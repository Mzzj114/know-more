from django.contrib import admin
from .models import Category, Post, Reply, Like, Favorite, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'post_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'category', 'view_count', 'reply_count',
        'like_count', 'is_pinned', 'is_locked', 'is_hidden',
        'created_at', 'last_reply_at'
    ]
    list_filter = ['is_pinned', 'is_locked', 'is_hidden', 'category', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    date_hierarchy = 'created_at'


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'post', 'author', 'floor', 'like_count',
        'is_hidden', 'created_at'
    ]
    list_filter = ['is_hidden', 'created_at']
    search_fields = ['content', 'author__username', 'post__title']
    raw_id_fields = ['author', 'post']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'post_count', 'reply_count', 'like_count',
        'created_at', 'updated_at'
    ]
    search_fields = ['user__username', 'signature']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'created_at']
    list_filter = ['content_type', 'created_at']
    search_fields = ['user__username']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title']


# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug', 'usage_count', 'created_at']
#     search_fields = ['name']
#     prepopulated_fields = {'slug': ('name',)}