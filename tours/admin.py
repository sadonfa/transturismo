from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Tours, Category, Include, Exclude, Cena, Comunitario, Review, TourImage, Newsletter, InspiratePlace

# 1. Inline para la galería de imágenes del tour
class TourImageInline(TabularInline):
    model = TourImage
    extra = 1
    verbose_name = "Imagen Adicional"
    verbose_name_plural = "Galería de Fotos Adicionales"


# 2. Administración del modelo Tours con galería integrada
@admin.register(Tours)
class ToursAdmin(ModelAdmin):
    list_display = (
        'id',
        'title',
        'slug',
        'cash',
        'is_offer',
        'time_start',
        'time_end',
        'order',
    )
    list_editable = ('is_offer', 'order')
    search_fields = ('title', 'description', 'info')
    list_filter = ('is_offer',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('category',)
    inlines = [TourImageInline]

@admin.register(InspiratePlace)
class InspiratePlaceAdmin(ModelAdmin):
    list_display = ('title', 'subtitle', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'subtitle')


# 3. Registro seguro de los demás modelos usando '__str__'
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('id', '__str__')

@admin.register(Include)
class IncludeAdmin(ModelAdmin):
    list_display = ('id', '__str__')

@admin.register(Exclude)
class ExcludeAdmin(ModelAdmin):
    list_display = ('id', '__str__')

@admin.register(Cena)
class CenaAdmin(ModelAdmin):
    list_display = ('id', '__str__')

@admin.register(Comunitario)
class ComunitarioAdmin(ModelAdmin):
    list_display = ('id', '__str__')

@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('author', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('author', 'comment')

@admin.register(Newsletter)
class NewsletterAdmin(ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('created_at',)