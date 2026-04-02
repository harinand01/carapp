from django import forms
from django.contrib.auth.models import User
from accounts.models import Mechanic

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class MechanicUpdateForm(forms.ModelForm):
    # Mechanic model currently has only services which are likely admin-managed
    # We can add fields here if the model changes, or display readonly info in template
    class Meta:
        model = Mechanic
        fields = [] # No specific fields to update for now
