from django.urls import path
from . import views

urlpatterns = [
    path('', views.doc_index, name='doc_index'),
    path('<slug:slug>/', views.doc_detail, name='doc_detail'),
]
