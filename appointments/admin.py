from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'barber_shop', 'service', 'date', 'start_time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('customer__user__email', 'barber_shop__name')
