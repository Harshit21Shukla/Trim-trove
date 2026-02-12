"""
Appointment models - Booking, status management
"""
from django.db import models
from django.utils import timezone
from authentication.models import Profile
from barbers.models import BarberShop, Service


class Appointment(models.Model):
    """Appointment booking between customer and barber shop."""

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    customer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='appointments_as_customer'
    )
    barber_shop = models.ForeignKey(
        BarberShop,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    date = models.DateField()
    start_time = models.TimeField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-start_time']

    def __str__(self):
        return f"{self.customer} - {self.barber_shop} - {self.date} {self.start_time} ({self.status})"

    @property
    def end_time(self):
        """Compute end time based on service duration."""
        from datetime import timedelta
        from django.utils import timezone as tz
        dt = tz.datetime.combine(self.date, self.start_time)
        dt += timedelta(minutes=self.service.duration_minutes)
        return dt.time()
