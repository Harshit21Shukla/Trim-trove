"""
Authentication models - Profile extends User with role (Customer/Barber)
"""
from django.db import models
from django.conf import settings


class Profile(models.Model):
    """Extended user profile with role and contact info."""

    class Role(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        BARBER = 'BARBER', 'Barber'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CUSTOMER
    )
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    @property
    def is_customer(self):
        return self.role == self.Role.CUSTOMER

    @property
    def is_barber(self):
        return self.role == self.Role.BARBER
