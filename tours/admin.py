from django.contrib import admin
from .models import Tours, Category, Include, Exclude, Cena

# Register your models here.

class ToursAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'update_at')
    list_display = ('title', 'order', 'created_at')

class CenaAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'update_at')
    list_display = ('title', 'order', 'created_at')

class CategoriesAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'update_at')
    list_display = ('title', 'created_at')

class IncludeAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'update_at')
    list_display = ('title', 'created_at')

class ExcludeAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'update_at')
    list_display = ('title', 'created_at')

admin.site.register(Include, IncludeAdmin)
admin.site.register(Exclude, ExcludeAdmin)
admin.site.register(Tours, ToursAdmin)
admin.site.register(Category, CategoriesAdmin)
admin.site.register(Cena, CenaAdmin)