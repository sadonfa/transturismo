from django.shortcuts import render, get_object_or_404
from tours.models import Tours
from .models import Booking
import hashlib
import requests

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

        booking = Booking(
            name = formulario['name'],
            lastname = formulario['lastname'],
            phone = formulario['phone'],
            mail = formulario['mail'],
            contry = formulario['contry'],
            city = formulario['city'],
            cash = formulario['cash'],
            tour = formulario['tour'],
            hotel = formulario['hotel'],
            adults = formulario['adults'],
            childre = formulario['childre'],
            total = total,
        ) 

        booking.save()

        pk = str(booking.pk).zfill(6)

        cadena = '{}{}00COPtest_integrity_FcbjBGNIK89XygOgPS7oXTyMHM8hOBgL'.format(pk,total)
        cadena.replace(" ","")
        
        m = hashlib.sha256()
        m.update(bytes(cadena, encoding='utf-8'))
        

        print(m.hexdigest())
        

    return render(request, 'det_booking.html', {
        'title': 'Detalles de Reserva',
        'booking': booking,
        'total': total,
        'pk_reservas': pk,
        'integrity': m.hexdigest(),
        'cadena': cadena
    })


def answer_booking(request, id=False):
    id_booking = id
    id_wompi = request.GET['id']
    # tour = get_object_or_404(Tours, id=53)
    # tour = Tours.objects.get(pk=id_booking) 
    URL_API =  "https://sandbox.wompi.co/v1/transactions/" + id_wompi

    response = requests.get(URL_API)

    print(response)
    print("---------------------------------")

    if response.status_code == 200:
          tour = response.json()
          for t in tour:
                print(t)
    else:
          tour = []

    print(tour)

    return render(request, 'respuesta.html', {
        'title': 'confirmacion de reserva',
        'id': id_wompi,
        'tour': tour
    })
