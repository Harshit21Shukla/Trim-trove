from django.contrib import admin
from .models import BarberShop, Service, WorkingHours


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1


class WorkingHoursInline(admin.TabularInline):
    model = WorkingHours
    extra = 0


@admin.register(BarberShop)
class BarberShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'address')
    inlines = [ServiceInline, WorkingHoursInline]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'barber_shop', 'price', 'duration_minutes')
    list_filter = ('barber_shop',)


@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ('barber_shop', 'day_of_week', 'start_time', 'end_time', 'is_closed')
