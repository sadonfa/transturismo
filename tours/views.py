from django.shortcuts import render, get_object_or_404
from .models import Tours, Category, Cena
import requests
# Create your views here.

def tours(request):
    tours = Tours.objects.all()
    if request.GET:
         
        id_wompi = request.GET['id']
        URL_API =  "https://sandbox.wompi.co/v1/transactions/" + id_wompi

        response = requests.get(URL_API)

        if response.status_code == 200:
            api = response.json()
            for t in api:
                    print(t)
    
    api = []

    return render(request, "tours/tours.html", {
        'title': 'Tours',
        'tours': tours,
        'api': api
    })

def tour(request, id, tour_slug):
    tour = Tours.objects.get(id=id)
    print(tour.category.all)
    return render(request, "tours/tour.html", {
        'title': 'Tour',
        'tour': tour
    })

def category(request, category_id):

    category = get_object_or_404(Category, id=category_id)

    return render(request, "tours/category.html", {
        'category' : category
    })

def cenas(request):
    
    cenas = Cena.objects.all()

    return render(request, "tours/cenas.html", {
        'title': 'Cenas',
        'cenas': cenas
    })