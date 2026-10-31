from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path
from . import views


urlpatterns = [
    path('tours/', views.tours, name="tours"),
    path('cenas/', views.cenas, name="cenas"),
    path('citytours/', views.citytours, name="citytours"),
    path('ofertas/', views.ofertas, name="ofertas"),
    path('comunitarios/', views.comunitario, name="comunitarios"),
    path('tour/<int:id>/<slug:tour_slug>/', views.tour, name='tour'),
    path('tours/categoria/<int:category_id>/', views.category, name="category"),
    path('api/tours/featured/', views.get_featured_tours, name='featured-tours'),
    path('api/tours/', views.get_all_tours, name='all-tours'),
    path('api/tours/home/', views.get_home_tours, name='home-tours'),
    path('api/newsletter/', views.subscribe_newsletter, name='subscribe-newsletter'),
    path('api/tours/<str:slug>/', views.get_tour_detail, name='tour-detail'),
    path('api/inspirate/', views.get_inspirate_places, name='inspirate-places'),
    path('api/tours/category/<str:category_slug>/', views.get_tours_by_category, name='tours-by-category'),
    path('api/categories/', views.get_categories, name='categories-list'),
    path('api/tours/category/<str:category_identifier>/', views.get_tours_by_category, name='tours-by-category'),

]
