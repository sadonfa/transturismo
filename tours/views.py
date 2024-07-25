from django.shortcuts import render
from .models import Tours
# Create your views here.

def tours(request):
    tours = Tours.objects.all()
    return render(request, "tours.html", {
        'title': 'Tours',
        'tours': tours
    })

def tour(request, id):
    tour = Tours.objects.get(id=id)
    return render(request, "tour.html", {
        'title': 'Tour',
        'tour': tour
    })