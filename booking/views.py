from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from tours.models import Tours, Cena
from .models import Booking
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from transturismo.settings import EMAIL_HOST_USER
import hashlib
import requests

# Create your views here.


def check(request, id=False, opc=False):   
    print(opc)
    if opc == 'dinner':
         tour = get_object_or_404(Cena, id=id)
    else:
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
            'checkin' : request.POST['checkin'],
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
            checkin = formulario['checkin'],
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

        

    return render(request, 'det_booking.html', {
        'title': 'Detalles de Reserva',
        'booking': booking,
        'total': total,
        'pk_reservas': pk,
        'integrity': m.hexdigest(),
        'cadena': cadena
    })


def answer_booking(request, id=False):
    
    id_wompi = request.GET['id']
    # tour = get_object_or_404(Tours, id=53)

    # URL_API =  "https://sandbox.wompi.co/v1/transactions/" + id_wompi
    URL_API =  "https://production.wompi.co/v1/transactions/" + id_wompi

    response = requests.get(URL_API)

    if response.status_code == 200:
          tour = response.json()
          for t in tour:
                print(t)
    else:
          tour = []

    # print(tour)
  
    id_booking = tour['data']['reference']
    id_booking = id_booking.lstrip('0')
    booking = Booking.objects.get(id=id_booking ) 

    if response.status_code == 200:

        subject = 'Nueva reserva de ' + booking.name 
        template = render_to_string(
            'correo.html',
            context={
                'nbooking': tour['data']['reference'],
                'name': booking.name ,      
                'correo': booking.mail,
                'content': booking.name,
                'lastname' : booking.lastname,
                'phone' : booking.phone,
                'contry' : booking.contry,
                'city' : booking.city,
                'cash' : booking.cash,
                'tour' : booking.tour,
                'checkin' : booking.checkin,
                'hotel' : booking.hotel,
                'adults' : booking.adults,
                'childre' : booking.childre,
                'total' : booking.total,
                'method' : tour['data']['payment_method']['type'] ,
                'card':tour['data']['payment_method']['extra']['name'] ,
                'card_type': tour['data']['payment_method']['extra']['card_type'],
                'data': tour['data']['finalized_at'],
                
                },
            )
        

        message = EmailMultiAlternatives(
            subject, #Titulo
            "This is an important message.",
            EMAIL_HOST_USER, #Remitente
            ["reservas@transturismocartagena.com.co", booking.mail]) #Destinatario

        message.attach_alternative(template, 'text/html')
        message.send()  

    return render(request, 'respuesta.html', {
        'title': 'confirmacion reserva',     
        'id': tour['data']['reference'],
        'tour': tour,
        'booking': booking          
    })

