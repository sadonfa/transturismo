from django.db import models
from transfers.models import Transfers, RutaTransporte

# Create your models here.

class Booking(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    lastname = models.CharField(max_length=200, verbose_name="Apellidos")
    phone = models.CharField(max_length=100, verbose_name="Teléfono")
    mail = models.EmailField(max_length=200, verbose_name="Correo")
    contry = models.CharField(max_length=200, verbose_name="País", default="Colombia")
    city = models.CharField(max_length=200, verbose_name="Ciudad", default="Cartagena")
    hotel = models.CharField(max_length=200, verbose_name="Hotel", blank=True, null=True)
    cash = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor", default=0)
    checkin = models.DateField(verbose_name="Checkin", null=True, blank=True)
    tour = models.CharField(max_length=200, verbose_name="Tours")
    adults = models.CharField(max_length=100, verbose_name="Adultos", default="1")
    childre = models.CharField(max_length=100, verbose_name="Niños", default="0")
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="total", default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado el")

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def __str__(self):
        return f'{self.name} {self.lastname} - {self.tour}'

    def get_id_formateado(self):
        return str(self.pk).zfill(6)

class BookingTransporte(models.Model):
    ESTADO_PAGO = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado / Confirmado'),
        ('RECHAZADO', 'Rechazado'),
    ]

    vehiculo = models.ForeignKey(Transfers, on_delete=models.PROTECT)
    ruta = models.ForeignKey(RutaTransporte, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Datos de la Reserva
    origen_custom = models.CharField(max_length=255, blank=True, null=True)
    destino_custom = models.CharField(max_length=255, blank=True, null=True)
    fecha_servicio = models.DateField()
    hora_servicio = models.TimeField()
    pasajeros = models.IntegerField(default=1)
    
    # Datos del Cliente
    nombre_completo = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=50)
    notas = models.TextField(blank=True, null=True)
    
    # Financiero y Estado
    total_cop = models.DecimalField(max_digits=12, decimal_places=2)
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO, default='PENDIENTE')
    referencia_pago = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)