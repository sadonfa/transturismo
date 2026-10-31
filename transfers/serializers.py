from rest_framework import serializers
from .models import Transfers, TarifaRuta

class TarifaRutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifaRuta
        fields = ['id', 'origen_zona', 'destino_zona', 'precio_cop', 'activo']

class TransfersSerializer(serializers.ModelSerializer):
    tarifas = TarifaRutaSerializer(many=True, read_only=True)

    class Meta:
        model = Transfers
        fields = '__all__'