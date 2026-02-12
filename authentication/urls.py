"""Authentication URL configuration."""
from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('signup/barber/', views.signup_view, {'role': 'barber'}, name='signup_barber'),
    path('signup/complete/', views.signup_complete, name='signup_complete'),
    path('logout/', views.logout_view, name='logout'),
]
