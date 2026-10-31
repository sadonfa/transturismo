from django.db import models
# from ckeditor.fields import RichTextField 
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify

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
    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True, verbose_name="URL Amigable (Slug)")
    description = models.CharField(max_length=250, verbose_name="Descripción Corta")
    category = models.ManyToManyField(Category, blank=True, verbose_name="Categorías")
    
    # Imagen de portada principal
    image1 = models.ImageField(upload_to="tours/", verbose_name="Imagen Principal (Portada)")
    
    info = CKEditor5Field('Información Detallada', config_name='tour_info', blank=True, null=True)
    
    # Incluye y No Incluye como texto multilínea
    include = models.TextField(
        verbose_name="Lo que Incluye (un elemento por línea)",
        blank=True, null=True,
        help_text="Escribe cada punto en una nueva línea (presiona Enter entre cada uno)."
    )
    noinclude = models.TextField(
        verbose_name="Lo que NO Incluye (un elemento por línea)",
        blank=True, null=True,
        help_text="Escribe cada exclusión en una nueva línea (presiona Enter entre cada uno)."
    )
    
    time_start = models.TimeField(verbose_name="Hora de salida", blank=True, null=True)
    time_end = models.TimeField(verbose_name="Hora de regreso", blank=True, null=True)
    cash = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor", default=0)
    order = models.IntegerField(default=0, verbose_name="Orden de aparición")
    cash = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio Oferta / Actual (COP)")
    original_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="Precio Regular Sin Descuento (COP)",
        help_text="Opcional. Llénalo solo si el tour tiene un precio anterior más alto para calcular el descuento."
    )
    order = models.IntegerField(default=0, verbose_name="Orden de aparición")
    is_offer = models.BooleanField(default=False, verbose_name="¿Es Oferta Especial?")
    is_offer = models.BooleanField(default=False, verbose_name="¿Es Oferta Especial?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado el")

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.cash:
            descuento = ((self.original_price - self.cash) / self.original_price) * 100
            return round(descuento)
        return 0
    
    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Tour"
        verbose_name_plural = "Tours"

    def __str__(self):
        return self.title

class TourImage(models.Model):
    tour = models.ForeignKey(Tours, related_name="gallery", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="tours/gallery/", verbose_name="Foto de Galería")

    class Meta:
        verbose_name = "Imagen de Galería"
        verbose_name_plural = "Imágenes de Galería"

class InspiratePlace(models.Model):
    title = models.CharField(max_length=150, verbose_name="Nombre del lugar emblemático")
    subtitle = models.CharField(max_length=200, verbose_name="Breve descripción o ubicación", blank=True, null=True)
    image = models.ImageField(upload_to="inspirate/", verbose_name="Fotografía")
    link = models.CharField(
        max_length=250, 
        verbose_name="Enlace opcional", 
        blank=True, 
        null=True,
        help_text="Ejemplo: /categoria/city-tours o la URL a un tour específico"
    )
    order = models.IntegerField(default=0, verbose_name="Orden de aparición")
    is_active = models.BooleanField(default=True, verbose_name="¿Mostrar en la web?")

    class Meta:
        verbose_name = "Lugar Emblemático (Inspírate)"
        verbose_name_plural = "Lugares Emblemáticos (Inspírate)"
        ordering = ['order', '-id']

    def __str__(self):
        return self.title
    
    
class Comunitario(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.CharField(max_length=250, verbose_name="Descripcion")
    category = models.ManyToManyField(Category, verbose_name="Categoria")
    image1 =  models.ImageField(default="null", upload_to="tours")
    image2 =  models.ImageField(default="null", upload_to="tours")
    image3 =  models.ImageField(default="null", upload_to="tours")
    image4 =  models.ImageField(default="null", upload_to="tours")
    info = CKEditor5Field( config_name='extends')
    order = models.SmallIntegerField(verbose_name="Orden", default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado el")

    class Meta:
        verbose_name="Comunitario"
        verbose_name_plural="Comunitarios"
        ordering=['order']

    def __str__(self):
        return f'{self.title}' 
    


class Cena(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.CharField(max_length=250, verbose_name="Descripcion")
    image1 =  models.ImageField(default="null", upload_to="tours")
    image2 =  models.ImageField(default="null", upload_to="tours")
    image3 =  models.ImageField(default="null", upload_to="tours")
    image4 =  models.ImageField(default="null", upload_to="tours")
    info = CKEditor5Field( config_name='extends')
    include = models.ManyToManyField(Include,  verbose_name="Incluye")
    noinclude = models.ManyToManyField(Exclude,  verbose_name="No Incluye")
    time_start = models.TimeField(verbose_name="Hora de salida", null=True, blank=True, default=timezone.now)
    time_end = models.TimeField( verbose_name="Hora de regreso", null=True, blank=True, default=timezone.now)
    cash = models.IntegerField(verbose_name="Valor", default=0)
    order = models.SmallIntegerField(verbose_name="Orden", default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Editado el")

    class Meta:
        verbose_name="Cena"
        verbose_name_plural="Cenas"
        ordering=['order']

    def __str__(self):
        return f'{self.title}' 
    


class Review(models.Model):
    author = models.CharField(max_length=100, verbose_name="Nombre del cliente")
    comment = models.TextField(verbose_name="Comentario")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="Calificación (1-5)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author} ({self.rating}★)"

class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Suscripción")

    class Meta:
        verbose_name = "Suscriptor del Boletín"
        verbose_name_plural = "Suscriptores del Boletín"

    def __str__(self):
        return self.email

    