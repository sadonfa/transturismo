from django.db import models

# Create your models here.
class HeroBanner(models.Model):
    title = models.CharField(max_length=150, verbose_name="Título Principal (Ej: CARTAGENA)")
    subtitle = models.CharField(max_length=150, blank=True, null=True, verbose_name="Texto Destacado (Ej: INSPIRA)")
    description = models.TextField(verbose_name="Descripción / Frase Corta")
    image = models.ImageField(upload_to="banners/", verbose_name="Imagen de Fondo")
    link_url = models.CharField(max_length=250, default="/ofertas", verbose_name="URL del Botón (ej: /ofertas o /tours/fenix)")
    order = models.IntegerField(default=0, verbose_name="Orden de Aparición")
    is_active = models.BooleanField(default=True, verbose_name="¿Banner Activo?")

    class Meta:
        verbose_name = "Banner Principal"
        verbose_name_plural = "Banners Principales"
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.title} {self.subtitle or ''}"