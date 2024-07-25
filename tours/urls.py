from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('tours', views.tours, name="tours"),
    path('tour/<int:id>/', views.tour, name='tour')
]
