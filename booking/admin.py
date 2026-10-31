from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Booking

# Register your models here.

@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    # Todos los campos expuestos en la tabla de resultados
    list_display = (
        'get_id_formateado',
        'tour',
        'name',
        'lastname',
        'phone',
        'mail',
        'checkin',
        'adults',
        'childre',
        'total',
        'created_at',
    )
    
    # Búsqueda rápida por cliente, correo, teléfono o tour
    search_fields = ('name', 'lastname', 'phone', 'mail', 'tour', 'hotel', 'city')
    
    # Filtros laterales convenientes
    list_filter = ('checkin', 'tour', 'contry', 'created_at')
    
    # Campos de solo lectura al ver el detalle de la reserva
    readonly_fields = ('created_at', 'update_at')
    
    # Orden predeterminado (más recientes primero)
    ordering = ('-created_at',)
    
    list_per_page = 25