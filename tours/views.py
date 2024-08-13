from django.shortcuts import render, get_object_or_404
from .models import Tours, Category
# Create your views here.

def tours(request):
    tours = Tours.objects.all()
    return render(request, "tours/tours.html", {
        'title': 'Tours',
        'tours': tours
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