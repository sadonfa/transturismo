from django.db import models
from ckeditor.fields import RichTextField 
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.CharField(max_length=250, verbose_name="Descripcion")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado el")

    class Meta:
        verbose_name="Categoria"
        verbose_name_plural="Categorias"
        ordering=['-created_at']

    def __str__(self):
        return f'{self.title}' 

class Include(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nombre")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado el")

    class Meta:
        verbose_name="Incluye"
        verbose_name_plural="Incluyes"
        ordering=['-created_at']

    def __str__(self):
        return f'{self.title}' 
    
class Exclude(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nombre")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado el")

    class Meta:
        verbose_name="No Incluye"
        verbose_name_plural="No Incluyes"
        ordering=['-created_at']

    def __str__(self):
        return f'{self.title}' 


class Tours(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.CharField(max_length=250, verbose_name="Descripcion")
    category = models.ManyToManyField(Category, verbose_name="Categoria", related_name="get_tour")
    image1 =  models.ImageField(default="null", upload_to="tours")
    image2 =  models.ImageField(default="null", upload_to="tours")
    image3 =  models.ImageField(default="null", upload_to="tours")
    image4 =  models.ImageField(default="null", upload_to="tours")
    info = CKEditor5Field(verbose_name="Info")
    include = models.ManyToManyField(Include,  verbose_name="Incluye")
    noinclude = models.ManyToManyField(Exclude,  verbose_name="No Incluye")
    time_start = models.TimeField(verbose_name="Hora de salida", null=True, blank=True, default=timezone.now)
    time_end = models.TimeField( verbose_name="Hora de regreso", null=True, blank=True, default=timezone.now)
    cash = models.IntegerField(verbose_name="Valor", default=0)
    order = models.SmallIntegerField(verbose_name="Orden", default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado el")

    class Meta:
        verbose_name="Tour"
        verbose_name_plural="Toures"
        ordering=['order']

    def __str__(self):
        return f'{self.title}' 
    


    