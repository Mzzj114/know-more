from django.urls import path
from . import views

urlpatterns = [
    path('', views.doc_index, name='doc_index'),
    path('<str:language>/<slug:slug>/', views.doc_detail, name='doc_detail'),
]
