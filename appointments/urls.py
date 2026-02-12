"""Appointments URL configuration."""
from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('slots/', views.available_slots, name='available_slots'),
    path('<int:pk>/cancel/', views.cancel_appointment, name='cancel'),
    path('<int:pk>/accept/', views.accept_appointment, name='accept'),
    path('<int:pk>/reject/', views.reject_appointment, name='reject'),
    path('<int:pk>/complete/', views.complete_appointment, name='complete'),
]
