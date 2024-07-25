from django.db import models
from ckeditor.fields import RichTextField 
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.CharField(max_length=250, verbose_name="Descripcion")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado el")

    def __str__(self):
        return f'{self.title}' 


class Tours(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.CharField(max_length=250, verbose_name="Descripcion")
    category = models.ManyToManyField(Category, blank=True, verbose_name="Categoria")
    image1 =  models.ImageField(default="null", upload_to="Imagen 1")
    # image2 =  models.ImageField(default="null", upload_to="Imagen 2")
    # image3 =  models.ImageField(default="null", upload_to="Imagen 3")
    # image4 =  models.ImageField(default="null", upload_to="Imagen 4")
    info = CKEditor5Field(verbose_name="Info")
    # include = models.ManyToManyField(Inclusiones, blank=True, verbose_name="Incluye")
    # noinclude = models.ManyToManyField(Exclusiones, blank=True, verbose_name="No Incluye")
    cash = models.IntegerField(verbose_name="Valor", default=0)
    # cash = MoneyField(max_digits=14, decimal_places=2, default_currency='COP', default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado el")

    def __str__(self):
        return f'{self.title}' 
    


    