from django.shortcuts import render
from tours.models import Tours, Cena

# Create your views here.

def home(request):
    lugares = Tours.objects.filter(title='Tierra Bomba')
    tours = Tours.objects.all()[0:6]
    ofertas = [
        Tours.objects.filter(title='Isla del encanto'),
        Tours.objects.filter(title='CITY TOUR HISTORICO'),
        Tours.objects.filter(title='TOUR BARÚ TERRESTRE')
    ]


    return render(request, "home.html",{
        'title': 'home',
        'tours': tours,
        'lugares': lugares,
        'ofertas': ofertas
    })