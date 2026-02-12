"""Barber forms - Shop, Service, WorkingHours"""
from django import forms
from django.forms import inlineformset_factory
from .models import BarberShop, Service, WorkingHours


class BarberShopForm(forms.ModelForm):
    class Meta:
        model = BarberShop
        fields = ('name', 'description', 'address', 'latitude', 'longitude', 'phone', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'address': forms.TextInput(attrs={'class': 'form-input'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.000001'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'description', 'price', 'duration_minutes')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'step': 1}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-input', 'min': 5, 'step': 5}),
        }


class WorkingHoursForm(forms.ModelForm):
    class Meta:
        model = WorkingHours
        fields = ('day_of_week', 'start_time', 'end_time', 'is_closed')
        widgets = {
            'day_of_week': forms.Select(attrs={'class': 'form-input'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'is_closed': forms.CheckboxInput(),
        }


WorkingHoursFormSet = inlineformset_factory(
    BarberShop,
    WorkingHours,
    form=WorkingHoursForm,
    extra=0,
    can_delete=True,
)
