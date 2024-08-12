from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class Page(models.Model):
    title = models.CharField(verbose_name="Titulo", max_length=200 )
    content = CKEditor5Field('Contenido', config_name='extends')
    order = models.SmallIntegerField(verbose_name="Orden", default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name="Pagina"
        verbose_name_plural="Paginas"
        ordering = ['order','title']

    def __str__(self):
        return self.title