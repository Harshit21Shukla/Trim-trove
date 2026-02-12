"""
Appointment views - Slots API, Cancel, Accept, Reject, Complete
"""
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.utils import timezone

from authentication.decorators import customer_required, barber_required
from .models import Appointment
from .utils import get_available_slots
from barbers.models import BarberShop, Service


@require_GET
@login_required
def available_slots(request):
    """
    API: GET ?shop_id=1&service_id=1&date=2025-01-15
    Returns JSON list of available slots.
    """
    shop_id = request.GET.get('shop_id')
    service_id = request.GET.get('service_id')
    date_str = request.GET.get('date')

    if not all([shop_id, service_id, date_str]):
        return JsonResponse({'error': 'Missing params'}, status=400)

    try:
        shop = BarberShop.objects.get(pk=shop_id)
        service = Service.objects.get(pk=service_id, barber_shop=shop)
        target_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
    except (BarberShop.DoesNotExist, Service.DoesNotExist, ValueError):
        return JsonResponse({'error': 'Invalid params'}, status=400)

    slots = get_available_slots(shop, service, target_date)
    data = [{'start': s[0].strftime('%H:%M'), 'end': s[1].strftime('%H:%M')} for s in slots]
    return JsonResponse({'slots': data})


@require_POST
@customer_required
def cancel_appointment(request, pk):
    """Customer cancels an appointment."""
    appointment = get_object_or_404(Appointment, pk=pk, customer=request.user.profile)
    if appointment.status in ('PENDING', 'ACCEPTED'):
        appointment.status = Appointment.Status.CANCELLED
        appointment.save()
    return redirect('customers:appointments')


@require_POST
@barber_required
def accept_appointment(request, pk):
    """Barber accepts an appointment."""
    profile = request.user.profile
    appointment = get_object_or_404(
        Appointment, pk=pk, barber_shop__created_by=profile
    )
    if appointment.status == 'PENDING':
        appointment.status = Appointment.Status.ACCEPTED
        appointment.save()
    return redirect('barbers:appointments')


@require_POST
@barber_required
def reject_appointment(request, pk):
    """Barber rejects an appointment."""
    profile = request.user.profile
    appointment = get_object_or_404(
        Appointment, pk=pk, barber_shop__created_by=profile
    )
    if appointment.status == 'PENDING':
        appointment.status = Appointment.Status.REJECTED
        appointment.save()
    return redirect('barbers:appointments')


@require_POST
@barber_required
def complete_appointment(request, pk):
    """Barber marks appointment as completed."""
    profile = request.user.profile
    appointment = get_object_or_404(
        Appointment, pk=pk, barber_shop__created_by=profile
    )
    if appointment.status == 'ACCEPTED':
        appointment.status = Appointment.Status.COMPLETED
        appointment.save()
    return redirect('barbers:appointments')
