from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # 身份验证
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),

    # 教程前端页面路由
    path('tutorial/', views.tutorial_page, name='tutorial'),
    path('tutorial/<str:slug>/', views.tutorial_page, name='tutorial_with_slug'),
    
    # 获取教程数据的 API
    path('api/tutorials/', views.api_tutorial_list, name='api_tutorial_list'),
    path('api/tutorials/<str:slug>/', views.api_tutorial_detail, name='api_tutorial_detail'),
]
