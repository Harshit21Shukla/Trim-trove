"""Customer URL configuration."""
from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('shops/', views.shop_list, name='shops'),
    path('shop/<int:pk>/', views.shop_detail, name='shop_detail'),
    path('book/<int:shop_id>/', views.book_appointment, name='book'),
    path('appointments/', views.appointments, name='appointments'),
]
