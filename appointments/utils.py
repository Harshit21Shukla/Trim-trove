"""
Appointment utilities - Slot generation, availability check
"""
from datetime import datetime, date, timedelta
from barbers.models import BarberShop, Service, WorkingHours


def get_available_slots(barber_shop, service, target_date):
    """
    Get available time slots for a barber shop on a given date.
    Returns list of (start_time, end_time) tuples.
    """
    # Get working hours for this day
    day_of_week = target_date.weekday()  # 0=Monday, 6=Sunday
    wh = WorkingHours.objects.filter(
        barber_shop=barber_shop,
        day_of_week=day_of_week,
        is_closed=False
    ).first()
    if not wh:
        return []

    # Build slots from start_time to end_time, each slot = service duration
    from appointments.models import Appointment
    duration = service.duration_minutes
    slots = []
    current = datetime.combine(target_date, wh.start_time)
    end_dt = datetime.combine(target_date, wh.end_time)

    while current + timedelta(minutes=duration) <= end_dt:
        slot_start = current.time()
        slot_end = (current + timedelta(minutes=duration)).time()

        # Check if slot is already booked
        is_booked = Appointment.objects.filter(
            barber_shop=barber_shop,
            date=target_date,
            start_time=slot_start,
            status__in=['PENDING', 'ACCEPTED']
        ).exists()

        # Don't offer past slots today
        now = datetime.now().time()
        if target_date == date.today() and slot_start <= now:
            is_booked = True

        if not is_booked:
            slots.append((slot_start, slot_end))

        current += timedelta(minutes=30)  # 30-min increment between slots

    return slots
