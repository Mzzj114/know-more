from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    


    # 教程前端页面路由
    path('tutorial/', views.tutorial_page, name='tutorial'),
    path('tutorial/<str:slug>/', views.tutorial_page, name='tutorial_with_slug'),
    
    # 获取教程数据的 API
    path('api/tutorials/', views.api_tutorial_list, name='api_tutorial_list'),
    path('api/tutorials/<str:slug>/', views.api_tutorial_detail, name='api_tutorial_detail'),
]
