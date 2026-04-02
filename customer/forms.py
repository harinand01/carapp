from django import forms
from .models import Vehicle
from accounts.models import Customer
from django.contrib.auth.models import User

class VehicleForm(forms.ModelForm):
    make = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Make'}))
    model = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Model'}))
    license_plate = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'License Plate'}))
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year'}))

    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'license_plate', 'year']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class CustomerUpdateForm(forms.ModelForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    class Meta:
        model = Customer
        fields = ['phone', 'address']
