from django.contrib import admin
from .models import HeroBanner

@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'subtitle', 'description')


admin.site.site_header = "Transturismo Cartagena"
admin.site.site_title = "Admin Transturismo"
admin.site.index_title = "Panel de Control y Operación"