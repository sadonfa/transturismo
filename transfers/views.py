from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Transfers, RutaTransporte
from .serializers import TransfersSerializer

# Create your views here.

@api_view(['GET'])
def get_transfers_api(request):
    """
    Retorna la lista completa de transportes ordenados según el campo 'order'
    """
    transfers = Transfers.objects.all().order_by('order', 'id')
    serializer = TransfersSerializer(transfers, many=True, context={'request': request})
    return Response(serializer.data)

def transfers(request):

    transfers = Transfers.objects.all()

    return render(request, 'transfers.html', {
        'title': 'Transportes',
        'vehiculos': transfers
    })


@api_view(['GET'])
def get_transfers_with_routes(request):
    """Devuelve transportes con sus rutas y tarifas integradas"""
    transfers = Transfers.objects.all().order_by('order', 'id')
    data = []
    
    for t in transfers:
        rutas = RutaTransporte.objects.filter(vehiculo=t, activo=True).values('id', 'origen', 'destino', 'precio_cop')
        data.append({
            'id': t.id,
            'name': t.name,
            'description': t.description,
            'image': t.image.url if t.image and t.image != 'null' else None,
            'rutas': list(rutas)
        })
        
    return Response(data)