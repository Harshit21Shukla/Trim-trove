"""
TrimTrove - Project-level views (Landing page)
"""
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User = get_user_model()


def landing_page(request):
    """Landing page - redirect logged-in users to their dashboard."""
    if request.user.is_authenticated:
        from authentication.models import Profile
        try:
            profile = Profile.objects.get(user=request.user)
            if profile.role == Profile.Role.BARBER:
                return redirect('barbers:dashboard')
            return redirect('customers:dashboard')
        except Profile.DoesNotExist:
            return redirect('auth:signup_complete')
    return render(request, 'landing.html')
