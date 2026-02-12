"""
TrimTrove - Main URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views as project_views

urlpatterns = [
    path('', project_views.landing_page, name='landing'),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls', namespace='auth')),
    path('customer/', include('customers.urls', namespace='customers')),
    path('barber/', include('barbers.urls', namespace='barbers')),
    path('appointments/', include('appointments.urls', namespace='appointments')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
