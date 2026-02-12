"""
Barber views - Dashboard, services, availability, appointments
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from authentication.decorators import barber_required
from .models import BarberShop, Service, WorkingHours
from .forms import BarberShopForm, ServiceForm, WorkingHoursFormSet
from appointments.models import Appointment


@barber_required
def dashboard(request):
    """Barber dashboard - overview of shop and appointments."""
    profile = request.user.profile
    shops = BarberShop.objects.filter(created_by=profile).prefetch_related('services')
    # Today's and upcoming appointments across all shops
    from django.utils import timezone
    appointments = Appointment.objects.filter(
        barber_shop__created_by=profile
    ).exclude(status__in=['CANCELLED', 'REJECTED']).select_related(
        'customer__user', 'service', 'barber_shop'
    ).order_by('date', 'start_time')[:20]
    return render(request, 'barbers/dashboard.html', {
        'shops': shops,
        'appointments': appointments,
    })


@barber_required
def shop_create(request):
    """Create a new barber shop."""
    profile = request.user.profile
    if request.method == 'POST':
        form = BarberShopForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.created_by = profile
            shop.save()
            return redirect('barbers:dashboard')
    else:
        form = BarberShopForm()
    return render(request, 'barbers/shop_form.html', {'form': form})


@barber_required
def shop_edit(request, pk):
    """Edit barber shop."""
    shop = get_object_or_404(BarberShop, pk=pk, created_by=request.user.profile)
    if request.method == 'POST':
        form = BarberShopForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            form.save()
            return redirect('barbers:dashboard')
    else:
        form = BarberShopForm(instance=shop)
    return render(request, 'barbers/shop_form.html', {'form': form, 'shop': shop})


@barber_required
def services(request, shop_id):
    """List and manage services for a shop."""
    shop = get_object_or_404(BarberShop, pk=shop_id, created_by=request.user.profile)
    services_list = shop.services.all()
    return render(request, 'barbers/services.html', {'shop': shop, 'services': services_list})


@barber_required
def service_add(request, shop_id):
    """Add a service."""
    shop = get_object_or_404(BarberShop, pk=shop_id, created_by=request.user.profile)
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.barber_shop = shop
            service.save()
            return redirect('barbers:services', shop_id=shop_id)
    else:
        form = ServiceForm()
    return render(request, 'barbers/service_form.html', {'form': form, 'shop': shop})


@barber_required
def service_edit(request, shop_id, pk):
    """Edit a service."""
    shop = get_object_or_404(BarberShop, pk=shop_id, created_by=request.user.profile)
    service = get_object_or_404(Service, pk=pk, barber_shop=shop)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('barbers:services', shop_id=shop_id)
    else:
        form = ServiceForm(instance=service)
    return render(request, 'barbers/service_form.html', {'form': form, 'shop': shop})


@barber_required
def service_delete(request, shop_id, pk):
    """Delete a service."""
    shop = get_object_or_404(BarberShop, pk=shop_id, created_by=request.user.profile)
    service = get_object_or_404(Service, pk=pk, barber_shop=shop)
    if request.method == 'POST':
        service.delete()
        return redirect('barbers:services', shop_id=shop_id)
    return redirect('barbers:services', shop_id=shop_id)


@barber_required
def availability(request, shop_id):
    """Set working hours for the shop."""
    shop = get_object_or_404(BarberShop, pk=shop_id, created_by=request.user.profile)
    # Ensure we have a WorkingHours record for each day
    from datetime import time
    for day in range(7):
        WorkingHours.objects.get_or_create(
            barber_shop=shop,
            day_of_week=day,
            defaults={'start_time': time(9, 0), 'end_time': time(20, 0), 'is_closed': (day == 6)}
        )
    if request.method == 'POST':
        formset = WorkingHoursFormSet(request.POST, instance=shop)
        if formset.is_valid():
            formset.save()
            return redirect('barbers:dashboard')
    else:
        formset = WorkingHoursFormSet(instance=shop)
    return render(request, 'barbers/availability.html', {'shop': shop, 'formset': formset})


@barber_required
def appointments(request):
    """View and manage appointments."""
    profile = request.user.profile
    appointments_list = Appointment.objects.filter(
        barber_shop__created_by=profile
    ).select_related('customer__user', 'service', 'barber_shop').order_by('-date', '-start_time')
    return render(request, 'barbers/appointments.html', {'appointments': appointments_list})
