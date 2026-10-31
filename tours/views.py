import requests
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Tours, Category, Review, Newsletter, InspiratePlace, Cena, Comunitario
from .serializers import TourSerializer, ReviewSerializer, InspiratePlaceSerializer, CategorySerializer


@api_view(['GET'])
def get_categories(request):
    """Retorna todas las categorías para el menú desplegable en React."""
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_tours_by_category(request, category_slug=None, **kwargs):
    identifier = category_slug or kwargs.get('category_identifier') or ""
    
    category_name = "Todas las Experiencias"
    
    # 1. Si se consulta la vista general de todas las experiencias
    if str(identifier).lower() in ['todas', 'all', 'experiencias', '']:
        tours = Tours.objects.all()
        serializer = TourSerializer(tours, many=True, context={'request': request})
        return Response({
            'category_name': 'Todas las Experiencias',
            'tours': serializer.data
        })

    # 2. Búsqueda por ID numérico de categoría
    if str(identifier).isdigit():
        cat_id = int(identifier)
        cat_obj = Category.objects.filter(id=cat_id).first()
        if cat_obj:
            category_name = cat_obj.title
            tours = Tours.objects.filter(category=cat_obj)
        else:
            tours = Tours.objects.none()

    # 3. Búsqueda por texto o slug
    else:
        clean_name = str(identifier).replace('-', ' ').strip()
        cat_obj = Category.objects.filter(title__icontains=clean_name).first()
        if cat_obj:
            category_name = cat_obj.title
            tours = Tours.objects.filter(category=cat_obj)
        else:
            category_name = clean_name.title()
            tours = Tours.objects.filter(category__title__icontains=clean_name)

    serializer = TourSerializer(tours.distinct(), many=True, context={'request': request})

    return Response({
        'category_name': category_name,
        'tours': serializer.data
    })

@api_view(['GET'])
def get_featured_tours(request):
    tours = Tours.objects.all()[:6]
    serializer = TourSerializer(tours, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def get_all_tours(request):
    tours = Tours.objects.all()
    serializer = TourSerializer(tours, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def get_home_tours(request):
    ofertas = Tours.objects.filter(is_offer=True)[:3]
    paraisos = Tours.objects.all()[:6]
    reviews = Review.objects.all()[:3]

    return Response({
        'ofertas': TourSerializer(ofertas, many=True, context={'request': request}).data,
        'paraisos': TourSerializer(paraisos, many=True, context={'request': request}).data,
        'reviews': ReviewSerializer(reviews, many=True, context={'request': request}).data,
    })


@api_view(['GET'])
def get_tour_detail(request, slug):
    try:
        if slug.isdigit():
            tour = Tours.objects.get(pk=int(slug))
        else:
            tour = Tours.objects.get(slug=slug)

        serializer = TourSerializer(tour, context={'request': request})
        return Response(serializer.data)

    except Tours.DoesNotExist:
        return Response({'error': 'Tour no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def subscribe_newsletter(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'El correo es requerido'}, status=status.HTTP_400_BAD_REQUEST)

    subscriber, created = Newsletter.objects.get_or_create(email=email)
    if not created:
        return Response({'message': 'El correo ya está suscrito'}, status=status.HTTP_200_OK)

    return Response({'message': 'Suscripción exitosa'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_inspirate_places(request):
    places = InspiratePlace.objects.filter(is_active=True)[:6]
    serializer = InspiratePlaceSerializer(places, many=True, context={'request': request})
    return Response(serializer.data)


# Vistas para renderizado de plantillas HTML clásicas de Django
def tours(request):
    tours_list = Tours.objects.all()
    api = []
    if request.GET and 'id' in request.GET:
        id_wompi = request.GET['id']
        URL_API = "https://sandbox.wompi.co/v1/transactions/" + id_wompi
        response = requests.get(URL_API)
        if response.status_code == 200:
            api = response.json()

    return render(request, "tours/tours.html", {
        'title': 'Tours',
        'tours': tours_list,
        'api': api
    })


def tour(request, id, tour_slug): 
    tour_obj = Tours.objects.get(id=id)
    return render(request, "tours/tour.html", {
        'title': 'Tour',
        'tour': tour_obj
    })


def category(request, category_id):
    category_obj = get_object_or_404(Category, id=category_id)
    return render(request, "tours/category.html", {
        'category': category_obj
    })


def cenas(request):
    cenas_list = Cena.objects.all()
    return render(request, "tours/cenas.html", {
        'title': 'Cenas',
        'cenas': cenas_list
    })


def citytours(request):
    citytours_list = Tours.objects.filter(category=4)
    return render(request, "tours/citytours.html", {
        'title': 'City Tours',
        'citytours': citytours_list
    })


def ofertas(request):
    ofertas_list = Tours.objects.filter(category=5)
    return render(request, "tours/ofertas.html", {
        'title': 'Ofertas',
        'ofertas': ofertas_list
    })


def comunitario(request):
    comunitario_list = Tours.objects.filter(category=6)
    comun = Comunitario.objects.all()
    return render(request, "tours/comunitarios.html", {
        'title': 'Comunitarios',
        'ofertas': comunitario_list,
        'comunitarios': comun 
    })


def botes(request):
    botes_list = Tours.objects.filter(category=7)
    return render(request, "tours/botes.html", {
        'title': 'Botes',
        'ofertas': botes_list
    })