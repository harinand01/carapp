from django.db import models
from accounts.models import Customer

class Vehicle(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=20, unique=True)
    year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"
