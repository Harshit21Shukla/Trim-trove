"""Customer forms - Booking"""
from django import forms
from appointments.models import Appointment


class BookingForm(forms.ModelForm):
    """Form to book an appointment."""

    def __init__(self, shop=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if shop:
            self.fields['service'].queryset = shop.services.all()
            self.fields['service'].widget.attrs.update({'class': 'form-input'})
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-input'})
        self.fields['start_time'].widget = forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'})
        self.fields['notes'].widget.attrs.update({'class': 'form-input', 'rows': 3, 'placeholder': 'Optional notes'})

    class Meta:
        model = Appointment
        fields = ('service', 'date', 'start_time', 'notes')
