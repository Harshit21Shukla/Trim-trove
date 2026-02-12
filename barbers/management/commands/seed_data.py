"""
Management command to seed sample data for TrimTrove.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from authentication.models import Profile
from barbers.models import BarberShop, Service, WorkingHours
from datetime import time

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed sample data for testing TrimTrove'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # Create barber user
        barber_user, created = User.objects.get_or_create(
            username='barber@trimtrove.com',
            defaults={
                'email': 'barber@trimtrove.com',
                'first_name': 'Raj',
                'last_name': 'Kumar',
            }
        )
        if created:
            barber_user.set_password('barber123')
            barber_user.save()
        try:
            barber_profile = barber_user.profile
        except Profile.DoesNotExist:
            barber_profile = Profile.objects.create(user=barber_user, role=Profile.Role.BARBER, phone='9876543210')
        if barber_profile.role != Profile.Role.BARBER:
            barber_profile.role = Profile.Role.BARBER
            barber_profile.save()

        # Create barber shop
        shop, _ = BarberShop.objects.get_or_create(
            name="Raj's Classic Cuts",
            defaults={
                'created_by': barber_profile,
                'description': 'Premium haircuts and grooming services in the heart of the city.',
                'address': '123 MG Road, Bangalore, Karnataka',
                'latitude': 12.9716,
                'longitude': 77.5946,
                'phone': '9876543210',
            }
        )
        if shop.created_by_id != barber_profile.pk:
            shop.created_by = barber_profile
            shop.save()

        # Create services
        services_data = [
            ('Haircut', 150, 30),
            ('Beard Trim', 80, 15),
            ('Haircut + Beard', 200, 45),
            ('Kids Haircut', 100, 25),
        ]
        for name, price, dur in services_data:
            Service.objects.get_or_create(
                barber_shop=shop,
                name=name,
                defaults={'price': price, 'duration_minutes': dur}
            )

        # Create working hours (Mon-Sat 9-8)
        for day in range(6):  # Mon-Sat
            WorkingHours.objects.get_or_create(
                barber_shop=shop,
                day_of_week=day,
                defaults={
                    'start_time': time(9, 0),
                    'end_time': time(20, 0),
                    'is_closed': False,
                }
            )
        WorkingHours.objects.get_or_create(
            barber_shop=shop,
            day_of_week=6,
            defaults={
                'start_time': time(9, 0),
                'end_time': time(20, 0),
                'is_closed': True,  # Sunday closed
            }
        )

        # Create second shop
        shop2, _ = BarberShop.objects.get_or_create(
            name="Style Studio",
            defaults={
                'created_by': barber_profile,
                'description': 'Modern cuts and styling.',
                'address': '45 Brigade Road, Bangalore',
                'latitude': 12.9750,
                'longitude': 77.6063,
                'phone': '9123456789',
            }
        )
        if shop2:
            for name, price, dur in [('Haircut', 200, 35), ('Beard', 100, 20)]:
                Service.objects.get_or_create(
                    barber_shop=shop2,
                    name=name,
                    defaults={'price': price, 'duration_minutes': dur}
                )
            for day in range(7):
                WorkingHours.objects.get_or_create(
                    barber_shop=shop2,
                    day_of_week=day,
                    defaults={
                        'start_time': time(10, 0),
                        'end_time': time(21, 0),
                        'is_closed': (day == 6),
                    }
                )

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write('Barber login: barber@trimtrove.com / password: barber123')
