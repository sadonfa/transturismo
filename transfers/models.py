from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class Transfers(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre del Vehículo")
    description = CKEditor5Field(config_name='extends', verbose_name="Descripción Comercial / Detalles", blank=True, null=True)
    
    # --- ESPECIFICACIONES DE CAPACIDAD Y AMENIDADES ---
    capacidad_pasajeros = models.IntegerField(default=4, verbose_name="Máximo Pasajeros (ej. 4)")
    capacidad_maletas = models.IntegerField(default=3, verbose_name="Máximo Maletas Grandes (ej. 3)")
    aire_acondicionado = models.BooleanField(default=True, verbose_name="¿Tiene Aire Acondicionado?")
    wifi = models.BooleanField(default=False, verbose_name="¿Tiene Wifi?")
    
    # --- TARIFAS BASE DE CONTINGENCIA ---
    tarifa_base = models.DecimalField(max_digits=12, decimal_places=2, default=45000, verbose_name="Tarifa Base (COP)")
    precio_km_extra = models.DecimalField(max_digits=12, decimal_places=2, default=3500, verbose_name="Valor por Km Extra (COP)")

    # --- IMÁGENES Y ORDEN ---
    image = models.ImageField(default="null", upload_to="transfers", verbose_name="Imagen Principal")
    image1 = models.ImageField(upload_to="transfers", blank=True, null=True)
    image2 = models.ImageField(upload_to="transfers", blank=True, null=True)
    order = models.IntegerField(default=0, verbose_name="Orden de Aparición")

    class Meta:
        verbose_name = "Vehículo / Transporte"
        verbose_name_plural = "Vehículos / Transportes"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.name} ({self.capacidad_pasajeros} pax)"

class RutaTransporte(models.Model):
    vehiculo = models.ForeignKey('Transfers', on_delete=models.CASCADE, related_name='rutas', verbose_name="Vehículo")
    origen = models.CharField(max_length=150, verbose_name="Lugar de Origen")
    destino = models.CharField(max_length=150, verbose_name="Lugar de Destino")
    precio_cop = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio (COP)")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Ruta de Transporte"
        verbose_name_plural = "Rutas de Transporte"

    def __str__(self):
        return f"{self.vehiculo.name}: {self.origen} -> {self.destino} (${self.precio_cop:,.0f} COP)"

class TarifaRuta(models.Model):
    vehiculo = models.ForeignKey(Transfers, on_delete=models.CASCADE, related_name='tarifas', verbose_name="Vehículo")
    origen_zona = models.CharField(max_length=150, verbose_name="Zona / Punto Origen (ej. Aeropuerto, Bocagrande, Laguito)")
    destino_zona = models.CharField(max_length=150, verbose_name="Zona / Punto Destino")
    precio_cop = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio Fijo (COP)")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Tarifa de Ruta Fija"
        verbose_name_plural = "Tarifas de Rutas Fijas"

    def __str__(self):
        return f"{self.vehiculo.name}: {self.origen_zona} -> {self.destino_zona} (${self.precio_cop:,.0f} COP)"