from django.shortcuts import render, get_object_or_404
from tours.models import Tours
from .models import Booking

# Create your views here.


def check(request, id=False):   

    tour = get_object_or_404(Tours, id=id)
    
    return render(request, 'check.html', {
        'title': 'Informacion de reserva',
        'tour': tour
    })


def det_booking(request):

    tour = Tours.objects.all()

    if request.method == 'POST':

        formulario = {
            'name' : request.POST['name'],
            'lastname' : request.POST['lastname'],
            'phone' : request.POST['phone'],
            'mail' : request.POST['mail'],
            'contry' : request.POST['contry'],
            'city' : request.POST['city'],
            'cash' : request.POST['cash'],
            'tour' : request.POST['tour'],
            'hotel' : request.POST['hotel'],
            'adults' : request.POST['adult'],
            'childre' : request.POST['childre'],
        }     

        total = int(formulario['adults']) * int(formulario['cash'])
        print(total)

    return render(request, 'det_booking.html', {
        'title': 'Detalles de Reserva',
        'booking': formulario,
        'total': total
    })


def answer_booking(request, id):
    return render(request, 'respuesta.html', {
        'tiitle': 'confirmacion de reserva',
        'id': id
    })
