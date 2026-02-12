"""
Role-based access decorators for TrimTrove
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Profile


def customer_required(view_func):
    """Decorator: user must be logged in and have Customer role."""
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            if profile.role != Profile.Role.CUSTOMER:
                return redirect('barbers:dashboard')
        except Profile.DoesNotExist:
            return redirect('auth:signup_complete')
        return view_func(request, *args, **kwargs)
    return _wrapped


def barber_required(view_func):
    """Decorator: user must be logged in and have Barber role."""
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            if profile.role != Profile.Role.BARBER:
                return redirect('customers:dashboard')
        except Profile.DoesNotExist:
            return redirect('auth:signup_complete')
        return view_func(request, *args, **kwargs)
    return _wrapped


def signup_complete_required(view_func):
    """Decorator: user must have a profile (completed signup)."""
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not Profile.objects.filter(user=request.user).exists():
            return redirect('auth:signup_complete')
        return view_func(request, *args, **kwargs)
    return _wrapped
