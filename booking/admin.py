from django.contrib import admin
from .models import Booking

# Register your models here.

class BookingAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'update_at')
    list_display = ('id','name', 'lastname', 'phone', 'tour', 'total', 'created_at')

admin.site.register(Booking, BookingAdmin)