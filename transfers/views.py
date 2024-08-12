from django.shortcuts import render
from .models import Transfers

# Create your views here.

def transfers(request):

    transfers = Transfers.objects.all()

    return render(request, 'transfers.html', {
        'title': 'Transportes',
        'vehiculos': transfers
    })