"""
Authentication forms - Login, Signup (Customer & Barber)
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class LoginForm(AuthenticationForm):
    """Login form with username (email) and password."""
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email address'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password'
        })
    )


class CustomerSignupForm(UserCreationForm):
    """Signup form for customers."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last name'})
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone (optional)'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Confirm password'})
        self.fields['email'].label = 'Email'
        # Replace username with email (use email as login identifier)
        if 'username' in self.fields:
            self.fields['username'] = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get('email')
        if email:
            cleaned['username'] = email
        return cleaned

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(username=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(user=user, role=Profile.Role.CUSTOMER, phone=self.cleaned_data.get('phone', ''))
        return user


class BarberSignupForm(UserCreationForm):
    """Signup form for barbers."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last name'})
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Confirm password'})
        if 'username' in self.fields:
            self.fields['username'] = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get('email')
        if email:
            cleaned['username'] = email
        return cleaned

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(username=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(user=user, role=Profile.Role.BARBER, phone=self.cleaned_data['phone'])
        return user


class SignupCompleteForm(forms.ModelForm):
    """Form for users without profile to complete signup."""
    role = forms.ChoiceField(choices=Profile.Role.choices, widget=forms.RadioSelect)

    class Meta:
        model = Profile
        fields = ('role', 'phone')
