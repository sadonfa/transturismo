from django.urls import path
from . import views

urlpatterns = [
    path('check/', views.check, name="check"),
    path('check/<int:id>/<str:opc>/', views.check, name="check"),
    path('detalles-reserva/', views.det_booking, name="detail_booking"),
    path('respuesta/', views.answer_booking, name="answer"),
    path('respuesta/<int:id>/', views.answer_booking, name="answer"),
    path('api/bookings/', views.create_booking, name='create-booking'),
    path('api/booking/create/', views.create_booking, name='create-booking'),
]