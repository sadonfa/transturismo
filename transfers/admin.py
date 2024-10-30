from django.contrib import admin
from .models import Transfers

# Register your models here.

class TransfersAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'created_at', )
    # list_display = '__all__'

admin.site.register(Transfers, TransfersAdmin)