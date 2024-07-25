from django.contrib import admin
from .models import Tours, Category

# Register your models here.

class ToursAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'update_at')

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'update_at')

admin.site.register(Tours, ToursAdmin)
admin.site.register(Category, CategoriesAdmin)