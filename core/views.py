from django.shortcuts import render
from tours.models import Tours, Cena
import requests

# Create your views here.

def home(request):
    lugares = Tours.objects.filter(title='Tierra Bomba')
    tours = Tours.objects.all()[0:6]
    ofertas = [
        Tours.objects.filter(title='Isla del encanto en islas del rosario'),
        Tours.objects.filter(title='CITY TOUR HISTORICO'),
        Tours.objects.filter(title='TOUR BARÚ TERRESTRE')
    ]


    return render(request, "home.html",{
        'title': 'home',
        'tours': tours,
        'lugares': lugares,
        'ofertas': ofertas
    })

def test(request):
    # response = requests.get('https://jsonplaceholder.typicode.com/posts')     
    # response = requests.get('https://mybusiness.googleapis.com/v4/{parent=accounts/*/locations/*}/reviews')
    response = requests.get('https://mybusiness.googleapis.com/v4/accounts/345438785308-9v1gu6pils5qjdqlrqnn1ihb2up8n94o.apps.googleusercontent.com/locations/{locationId}/reviews') 

    if response.status_code == 200:  
        data = response.json()  
    else:  
        data="Error retrieving data"

    return render(request, "test.html", {
        'title': 'test',
        'data': data
    })