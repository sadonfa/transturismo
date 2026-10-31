from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.urls import reverse
from tours.models import Tours, Cena
from .serializers import BookingSerializer
from .models import Booking
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from transturismo.settings import EMAIL_HOST_USER
from .utils import enviar_correos_confirmacion
import hashlib
import requests
import time


WOMPI_PUBLIC_KEY = getattr(settings, 'WOMPI_PUBLIC_KEY')
WOMPI_PRIVATE_KEY = getattr(settings, 'WOMPI_PRIVATE_KEY')
WOMPI_INTEGRITY_SECRET = getattr(settings, 'WOMPI_INTEGRITY_SECRET')
WOMPI_BASE_URL = getattr(settings, 'WOMPI_BASE_URL')

@api_view(['POST'])
@permission_classes([AllowAny])
def create_booking(request):
    data = request.data
    
    token_tarjeta = data.get('token_tarjeta') or data.get('token')
    total = data.get('total')
    email_cliente = data.get('mail')

    if not token_tarjeta or not total or not email_cliente:
        return Response({"error": "Faltan datos requeridos (token de tarjeta, correo o total)."}, status=status.HTTP_400_BAD_REQUEST)

    monto_centavos = int(float(total)) * 100
    moneda = "COP"
    tiempo_actual = int(time.time() * 1000)
    referencia_unica = f"TRST_{tiempo_actual}"

    cadena_a_firmar = f"{referencia_unica}{monto_centavos}{moneda}{WOMPI_INTEGRITY_SECRET}"
    firma_sha256 = hashlib.sha256(cadena_a_firmar.encode('utf-8')).hexdigest()

    headers = {
        "Authorization": f"Bearer {WOMPI_PRIVATE_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # 1. Obtener token de aceptación presignado
        merchant_res = requests.get(f"{WOMPI_BASE_URL}/merchants/{WOMPI_PUBLIC_KEY}")
        merchant_data = merchant_res.json()
        acceptance_token = merchant_data.get('data', {}).get('presigned_acceptance', {}).get('acceptance_token')

        if not acceptance_token:
            return Response({"error": "No se pudo obtener el token de aceptación de Wompi."}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Enviar la transacción a Wompi servidor a servidor
        payload = {
            "amount_in_cents": monto_centavos,
            "currency": moneda,
            "customer_email": email_cliente,
            "payment_method": {
                "type": "CARD",
                "token": token_tarjeta,
                "installments": 1
            },
            "reference": referencia_unica,
            "acceptance_token": acceptance_token,
            "signature": firma_sha256
        }

        response = requests.post(f"{WOMPI_BASE_URL}/transactions", json=payload, headers=headers)
        data_wompi = response.json()
        estado_transaccion = data_wompi.get('data', {}).get('status')

        # 3. Guardar reserva en BD si la transacción fue exitosa
        if response.status_code == 201 and estado_transaccion in ['APPROVED', 'PENDING']:
            transaccion_id = data_wompi['data']['id']

            booking = Booking.objects.create(
                name=data.get('name'),
                lastname=data.get('lastname'),
                phone=data.get('phone'),
                mail=email_cliente,
                contry=data.get('contry', 'Colombia'),
                city=data.get('city', 'Cartagena'),
                hotel=data.get('hotel', 'No especificado'),
                cash=data.get('cash', 0),
                checkin=data.get('checkin'),
                tour=data.get('tour'),
                adults=data.get('adults', '1'),
                childre=data.get('childre', '0'),
                total=total
            )

            try:
                enviar_correos_confirmacion(data, referencia_unica)
            except Exception as e:
                print(f"Error al enviar los correos de confirmación: {e}")

            return Response({
                "mensaje": "¡Pago procesado y reserva confirmada exitosamente!",
                "transaccion_id": transaccion_id,
                "reference": referencia_unica,
                "estado": estado_transaccion,
                "booking_id": booking.id
            }, status=status.HTTP_200_OK)

        else:
            error_data = data_wompi.get('error', {})
            error_msg = error_data.get('messages', 'El pago fue rechazado por la entidad bancaria.')
            return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"Error procesando pago: {e}")
        return Response({"error": f"Error interno en el servidor: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

        cadena = '{}{}{}00COP{}'.format(str(booking.pk).zfill(6), total, WOMPI_INTEGRITY_SECRET)
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
    # URL_API =  "https://production.wompi.co/v1/transactions/" + id_wompi
    URL_API = f"{WOMPI_BASE_URL}/transactions/{id_wompi}"

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

