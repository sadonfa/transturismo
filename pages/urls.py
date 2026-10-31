from django.urls import path
from . import views

urlpatterns = [
    path('page/<int:page_id>/<slug:page_slug>/', views.sample, name="page"),
    path('api/pages/', views.get_pages, name='pages-list'),
    path('api/pages/<str:slug>/', views.get_page_detail, name='page-detail'),
]

