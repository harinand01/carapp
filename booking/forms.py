from django import forms
from .models import Booking
from customer.models import Vehicle
from django.utils import timezone

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['vehicle', 'service', 'booking_date', 'time_slot', 'notes']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'time_slot': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'customer'):
            self.fields['vehicle'].queryset = Vehicle.objects.filter(customer=user.customer)
        else:
             self.fields['vehicle'].queryset = Vehicle.objects.none()

    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        if booking_date and booking_date < timezone.now().date():
            raise forms.ValidationError("You cannot book a service for a past date.")
        return booking_date

    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('booking_date')
        time_slot = cleaned_data.get('time_slot')

        if booking_date and time_slot:
            # Check if booking is for today
            if booking_date == timezone.now().date():
                current_time = timezone.now().time()
                # Check if the time slot start time has passed
                if time_slot.start_time < current_time:
                    raise forms.ValidationError({
                        'time_slot': "This time slot has already passed for today."
                    })
        return cleaned_data
