from django.contrib import admin
from .models import Service, TimeSlot, Booking, Payment

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'service', 'mechanic', 'status', 'booking_date')
    list_filter = ('status', 'booking_date', 'service')
    search_fields = ('customer__user__username', 'vehicle__license_plate')

admin.site.register(Service)
admin.site.register(TimeSlot)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Payment)
