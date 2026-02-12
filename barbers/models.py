"""
Barber models - BarberShop, Service, WorkingHours
"""
from django.db import models
from authentication.models import Profile


class BarberShop(models.Model):
    """Barber shop / salon owned by a barber."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=500)
    # For "nearby" feature - lat/lng (India coordinates)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    image = models.ImageField(upload_to='shops/', blank=True, null=True)
    created_by = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='barber_shops'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def avg_rating(self):
        """Average rating - placeholder for future Review model."""
        return 4.5


class Service(models.Model):
    """Service offered by a barber shop (haircut, beard, etc.)."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_minutes = models.PositiveIntegerField(default=30, help_text='Duration in minutes')
    barber_shop = models.ForeignKey(
        BarberShop,
        on_delete=models.CASCADE,
        related_name='services'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        unique_together = [['barber_shop', 'name']]

    def __str__(self):
        return f"{self.name} - ₹{self.price} ({self.duration_minutes} mins)"


class WorkingHours(models.Model):
    """Working hours for each day of the week."""
    class Day(models.IntegerChoices):
        MONDAY = 0, 'Monday'
        TUESDAY = 1, 'Tuesday'
        WEDNESDAY = 2, 'Wednesday'
        THURSDAY = 3, 'Thursday'
        FRIDAY = 4, 'Friday'
        SATURDAY = 5, 'Saturday'
        SUNDAY = 6, 'Sunday'

    barber_shop = models.ForeignKey(
        BarberShop,
        on_delete=models.CASCADE,
        related_name='working_hours'
    )
    day_of_week = models.IntegerField(choices=Day.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_closed = models.BooleanField(default=False, help_text='Mark as closed on this day')

    class Meta:
        ordering = ['day_of_week']
        unique_together = [['barber_shop', 'day_of_week']]
        verbose_name_plural = 'Working hours'

    def __str__(self):
        if self.is_closed:
            return f"{self.get_day_of_week_display()} - Closed"
        return f"{self.get_day_of_week_display()} - {self.start_time} to {self.end_time}"
