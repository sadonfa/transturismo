from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('transporte/', views.transfers, name="transfers"),
    path('api/transporte/', views.get_transfers_api, name='transfers-api-list'),
]
