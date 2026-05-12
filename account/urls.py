from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('api/send-code/', views.send_verify_code, name='send_verify_code'),
    path('api/send-reset-code/', views.send_reset_code, name='send_reset_code'),
]
