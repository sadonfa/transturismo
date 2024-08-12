from django.contrib import admin
from .models import Transfers

# Register your models here.

class TransfersAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'update_at')
    # list_display = '__all__'

admin.site.register(Transfers, TransfersAdmin)