from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('inicio/', views.home, name="home"),
    path('test/', views.test, name="test")
]
