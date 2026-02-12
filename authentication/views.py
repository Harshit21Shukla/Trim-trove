"""
Authentication views - Login, Signup, Logout
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .forms import LoginForm, CustomerSignupForm, BarberSignupForm, SignupCompleteForm
from .models import Profile


def redirect_after_login(request):
    """Redirect user to appropriate dashboard based on role."""
    try:
        profile = Profile.objects.get(user=request.user)
        if profile.role == Profile.Role.BARBER:
            return redirect('barbers:dashboard')
        return redirect('customers:dashboard')
    except Profile.DoesNotExist:
        return redirect('auth:signup_complete')


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect_after_login(request)

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect_after_login(request)

    return render(request, 'auth/login.html', {'form': form})


@require_http_methods(["GET", "POST"])
def signup_view(request, role='customer'):
    """Handle user signup (customer or barber)."""
    if request.user.is_authenticated:
        return redirect_after_login(request)

    FormClass = BarberSignupForm if role == 'barber' else CustomerSignupForm
    form = FormClass(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect_after_login(request)

    return render(request, 'auth/signup.html', {'form': form, 'role': role})


@login_required
@require_http_methods(["GET", "POST"])
def signup_complete(request):
    """Complete profile for users who signed up before profile existed."""
    if Profile.objects.filter(user=request.user).exists():
        return redirect_after_login(request)

    form = SignupCompleteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        return redirect_after_login(request)

    return render(request, 'auth/signup_complete.html', {'form': form})


@require_http_methods(["POST", "GET"])
def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('auth:login')
