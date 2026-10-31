from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('inicio/', views.home, name="home"),
    path('test/', views.test, name="test"),
    path('api/banners/', views.get_banners, name='banners-list'),
    path('api/resenas/', views.get_google_reviews, name='resenas-google'),
    path('api/chat/', views.chat_bot, name='chat_bot'),
]
