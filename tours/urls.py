from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('tours/', views.tours, name="tours"),
    path('cenas/', views.cenas, name="cenas"),
    path('citytours/', views.citytours, name="citytours"),
    path('ofertas/', views.ofertas, name="ofertas"),
    path('comunitarios/', views.comunitario, name="comunitarios"),
    path('tour/<int:id>/<slug:tour_slug>/', views.tour, name='tour'),
    path('tours/categoria/<int:category_id>/', views.category, name="category")

]
