from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    # ==================== 页面视图 ====================
    path('', views.forum_index, name='forum_index'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    
    # 发帖/编辑/删除
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    
    # 回复
    path('post/<int:post_pk>/reply/', views.create_reply, name='create_reply'),
    
    # 用户相关
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('user/profile/edit/', views.edit_profile, name='edit_profile'),
    path('my-favorites/', views.my_favorites, name='my_favorites'),
    
    # ==================== API 接口 ====================
    # 分类和帖子
    path('api/categories/', views.api_category_list, name='api_category_list'),
    path('api/posts/', views.api_post_list, name='api_post_list'),
    path('api/posts/<int:pk>/', views.api_post_detail, name='api_post_detail'),
    
    # 互动功能
    path('api/<str:content_type>/<int:object_id>/like/', views.api_like_toggle, name='api_like_toggle'),
    path('api/posts/<int:post_id>/favorite/', views.api_favorite_toggle, name='api_favorite_toggle'),
    
    # 回复 API
    path('api/posts/<int:post_id>/reply/', views.api_create_reply, name='api_create_reply'),
]