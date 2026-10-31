from django.contrib import admin
from .models import Transfers,RutaTransporte, TarifaRuta

# Register your models here.


@admin.register(RutaTransporte)
class RutaTransporteAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'origen', 'destino', 'precio_cop', 'activo')
    list_filter = ('vehiculo', 'activo')
    search_fields = ('origen', 'destino')

class TarifaRutaInline(admin.TabularInline):
    model = TarifaRuta
    extra = 1

@admin.register(Transfers)
class TransfersAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacidad_pasajeros', 'capacidad_maletas', 'tarifa_base', 'order')
    list_editable = ('capacidad_pasajeros', 'capacidad_maletas', 'tarifa_base', 'order')
    search_fields = ('name',)
    inlines = [TarifaRutaInline]