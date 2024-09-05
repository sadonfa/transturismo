from django.shortcuts import render
from tours.models import Tours, Cena

# Create your views here.

def home(request):
    lugares = Cena.objects.all()[0:3]
    tours = Tours.objects.all()[0:6]

    return render(request, "home.html",{
        'title': 'home',
        'tours': tours,
        'lugares': lugares
    })