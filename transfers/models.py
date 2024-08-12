from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class Transfers(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = CKEditor5Field(verbose_name="Info")
    image =  models.ImageField(default="null", upload_to="Imagen")
    image1 =  models.ImageField(default="null", upload_to="Imagen1")
    image2 =  models.ImageField(default="null", upload_to="Imagen2")
    image3 =  models.ImageField(default="null", upload_to="Imagen3")
    image4 =  models.ImageField(default="null", upload_to="Imagen4")
    image5 =  models.ImageField(default="null", upload_to="Imagen5")
    order = models.IntegerField(default=0, verbose_name="Orden")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado el")

    def __str__(self):
        return f'{self.name}' 