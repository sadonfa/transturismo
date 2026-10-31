from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from tours.models import Tours, Cena
from .models import HeroBanner
from tours.models import Tours
from transfers.models import Transfers
from openai import OpenAI
import json
import os
import requests
from django.conf import settings
from .serializers import HeroBannerSerializer

# Create your views here.

GOOGLE_PLACE_ID = getattr(settings, 'GOOGLE_PLACE_ID')
GOOGLE_API_KEY = getattr(settings, 'GOOGLE_API_KEY')

def generar_prompt_transporte():
    vehiculos = Transfers.objects.prefetch_related('tarifas').all()
    contexto = "\n--- FLOTA Y TARIFAS DE TRANSPORTE TRANSTURISMO ---\n"
    
    for v in vehiculos:
        contexto += f"\n- Vehículo: {v.name}\n"
        contexto += f"  Capacidad: {v.capacidad_pasajeros} pasajeros, {v.capacidad_maletas} maletas.\n"
        contexto += f"  Tarifa Base: ${v.tarifa_base:,.0f} COP | Km Extra: ${v.precio_km_extra:,.0f} COP.\n"
        
        # Rutas fijas asignadas
        tarifas_fijas = v.tarifas.filter(activo=True)
        if tarifas_fijas.exists():
            contexto += "  Tarifas Fijas Registradas:\n"
            for tf in tarifas_fijas:
                contexto += f"    * {tf.origen_zona} -> {tf.destino_zona}: ${tf.precio_cop:,.0f} COP\n"
                
    return contexto

@api_view(['POST'])
def chat_bot(request):
    user_message = request.data.get('message', '').strip()

    if not user_message:
        return Response({'error': 'El mensaje no puede estar vacío.'}, status=400)

    # 1. Obtener catálogo de Tours
    try:
        tours_db = Tours.objects.all()
        catalogo_tours = ""
        for tour in tours_db:
            catalogo_tours += f"- Tour: {tour.title} (URL: '/tours/{tour.slug}'). Precio: ${tour.cash} COP. Incluye: {tour.include}\n"
    except Exception as e:
        catalogo_tours = "- Isla Múcura (URL: '/tours/mucura'): $320.000 COP p.p."

    # 2. Obtener catálogo detallado y tarifas de Transporte desde la base de datos
    catalogo_transporte_detallado = generar_prompt_transporte()

    # 3. Prompt de instrucciones ÚNICO para la IA
    system_prompt = f"""
Eres el asistente virtual oficial de 'Transturismo Cartagena'. Tu objetivo es asesorar amablemente a los clientes, recomendar traslados privados y tours, e indicar las tarifas exactas.

Catálogo de TOURS disponibles:
{catalogo_tours}

Catálogo y Tarifas de TRANSPORTE disponibles:
{catalogo_transporte_detallado}

Instrucciones de respuesta:
1. Sé muy cordial, conciso y directo en español.
2. Recomienda el tour o servicio de transporte correspondiente indicando sus precios u opciones según la cantidad de pasajeros/maletas.
3. Devuelve SIEMPRE la respuesta en formato JSON estrictamente con esta estructura:
   {{
     "respuesta": "Texto explicativo para el usuario",
     "url_destino": "/tours/slug" o "/transporte" o null,
     "texto_boton": "Ver Tour y Reservar" o "Ver Transporte" o null
   }}
"""

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )

        content = json.loads(response.choices[0].message.content)
        return Response(content, status=200)

    except Exception as e:
        return Response({'error': f"Error al procesar la solicitud: {str(e)}"}, status=500)

@api_view(['GET'])
def get_google_reviews(request):
    url = (
        f"https://maps.googleapis.com/maps/api/place/details/json"
        f"?placeid={GOOGLE_PLACE_ID}"
        f"&fields=reviews,rating,user_ratings_total"
        f"&language=es"
        f"&key={GOOGLE_API_KEY}"
    )
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('status') == 'OK':
            result = data.get('result', {})
            raw_reviews = result.get('reviews', [])
            
            formatted_reviews = [
                {
                    'id': r.get('time'),
                    'nombre_cliente': r.get('author_name'),
                    'ciudad_origen': 'Cliente verificado en Google',
                    'comentario': r.get('text'),
                    'calificacion': r.get('rating'),
                    'foto': r.get('profile_photo_url'),
                    'tiempo': r.get('relative_time_description', ''),
                }
                for r in raw_reviews
            ]
            
            return Response({
                'rating_general': result.get('rating'),
                'total_resenas': result.get('user_ratings_total'),
                'reviews': formatted_reviews
            })
            
        return Response({
            'error': data.get('error_message', 'No se pudieron obtener las reseñas de Google')
        }, status=400)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_banners(request):
    banners = HeroBanner.objects.filter(is_active=True).order_by('order', '-id')
    serializer = HeroBannerSerializer(banners, many=True, context={'request': request})
    return Response(serializer.data)

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