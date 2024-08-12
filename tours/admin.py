from django.contrib import admin
from .models import Tours, Category, Include, Exclude

# Register your models here.

class ToursAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'update_at')
    list_display = ('title', 'created_at')

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