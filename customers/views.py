"""
Customer views - Dashboard, shops, booking, appointment history
"""
from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from authentication.decorators import customer_required
from barbers.models import BarberShop, Service
from appointments.models import Appointment
from appointments.utils import get_available_slots
from .forms import BookingForm


@customer_required
def dashboard(request):
    """Customer dashboard - nearby barber shops."""
    shops = BarberShop.objects.all().select_related('created_by').prefetch_related('services')
    return render(request, 'customers/dashboard.html', {'shops': shops})


@customer_required
def shop_list(request):
    """List all barber shops with search/filter."""
    q = request.GET.get('q', '')
    shops = BarberShop.objects.all().prefetch_related('services')
    if q:
        shops = shops.filter(
            Q(name__icontains=q) | Q(address__icontains=q)
        )
    return render(request, 'customers/shop_list.html', {'shops': shops, 'query': q})


@customer_required
def shop_detail(request, pk):
    """Barber shop detail with services and book button."""
    shop = get_object_or_404(BarberShop.objects.prefetch_related('services', 'working_hours'), pk=pk)
    return render(request, 'customers/shop_detail.html', {'shop': shop})


@customer_required
def book_appointment(request, shop_id):
    """Book appointment - select service, date, time."""
    shop = get_object_or_404(BarberShop.objects.prefetch_related('services', 'working_hours'), pk=shop_id)
    profile = request.user.profile

    if request.method == 'POST':
        form = BookingForm(shop=shop, data=request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.customer = profile
            appointment.barber_shop = shop
            appointment.save()
            return redirect('customers:appointments')
    else:
        initial = {}
        if request.GET.get('service'):
            try:
                svc = shop.services.get(pk=request.GET['service'])
                initial['service'] = svc
            except (ValueError, Service.DoesNotExist):
                pass
        form = BookingForm(shop=shop, initial=initial)

    # Min date = today
    min_date = date.today()
    max_date = date.today() + timedelta(days=30)
    return render(request, 'customers/book.html', {
        'shop': shop,
        'form': form,
        'min_date': min_date,
        'max_date': max_date,
    })


@customer_required
def appointments(request):
    """Customer appointment history."""
    profile = request.user.profile
    appointments_list = Appointment.objects.filter(
        customer=profile
    ).select_related('barber_shop', 'service').order_by('-date', '-start_time')
    return render(request, 'customers/appointments.html', {'appointments': appointments_list})
