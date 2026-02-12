"""Barber URL configuration."""
from django.urls import path
from . import views

app_name = 'barbers'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('shop/new/', views.shop_create, name='shop_create'),
    path('shop/<int:pk>/edit/', views.shop_edit, name='shop_edit'),
    path('shop/<int:shop_id>/services/', views.services, name='services'),
    path('shop/<int:shop_id>/services/add/', views.service_add, name='service_add'),
    path('shop/<int:shop_id>/services/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('shop/<int:shop_id>/services/<int:pk>/delete/', views.service_delete, name='service_delete'),
    path('shop/<int:shop_id>/availability/', views.availability, name='availability'),
    path('appointments/', views.appointments, name='appointments'),
]
