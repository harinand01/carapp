from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking, Mechanic, Payment, Service
from .forms import BookingForm
from django.contrib import messages
import random

def service_list(request):
    services = Service.objects.all()
    return render(request, 'booking/service_list.html', {'services': services})

@login_required
def book_service(request):
    if not hasattr(request.user, 'customer'):
        return redirect('login_redirect')

    if request.method == 'POST':
        form = BookingForm(request.user, request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user.customer
            
            # Mechanic Assignment Logic
            service = booking.service
            date = booking.booking_date
            time_slot = booking.time_slot
            
            # Find mechanics for this service
            mechanics = Mechanic.objects.filter(services=service)
            
            # Filter available mechanics
            available_mechanics = []
            for mech in mechanics:
                # Check if mech has booking at this time
                if not Booking.objects.filter(mechanic=mech, booking_date=date, time_slot=time_slot).exclude(status__in=['COMPLETED', 'DELIVERED']).exists():
                    available_mechanics.append(mech)
            
            if available_mechanics:
                booking.mechanic = random.choice(available_mechanics)
                booking.status = 'PENDING'
                booking.save()
                
                Payment.objects.create(booking=booking, amount=service.cost, is_successful=False)
                
                from carservice.utils import log_activity, get_client_ip, send_log
                ip = get_client_ip(request)
                log_activity(f"Service booked by {request.user.username} (Service: {service.name}) from {ip}")
                send_log("BOOKING_CREATED", ip, request.user.username)
                
                messages.success(request, f"Booking created! Assigned to {booking.mechanic}")
                return redirect('customer_dashboard')
            else:
                from carservice.utils import log_activity, get_client_ip, send_log
                ip = get_client_ip(request)
                log_activity(f"Booking failed by {request.user.username} (No mechanics available) from {ip}")
                send_log("BOOKING_FAILED", ip, request.user.username)
                messages.error(request, "No mechanics available for this service and time slot.")
    else:
        initial_data = {}
        service_id = request.GET.get('service_id')
        if service_id:
            try:
                service_id = int(service_id)
                initial_data['service'] = service_id
            except (ValueError, TypeError):
                pass
                
        form = BookingForm(request.user, initial=initial_data)
    
    return render(request, 'booking/book_service.html', {'form': form})

@login_required
def payment_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user.customer)
    try:
        payment = booking.payment
    except Payment.DoesNotExist:
        payment = None
        
    if request.method == 'POST':
        # Simulate payment
        if payment:
            payment.is_successful = True
            payment.save()
            
            from carservice.utils import log_activity, get_client_ip, send_log
            ip = get_client_ip(request)
            log_activity(f"Payment successful by {request.user.username} for booking {booking.id} from {ip}")
            send_log("PAYMENT_SUCCESSFUL", ip, request.user.username)
            
            messages.success(request, "Payment successful!")
            return redirect('customer_dashboard')

    return render(request, 'booking/payment_status.html', {'booking': booking, 'payment': payment})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user.customer)
    
    if booking.status == 'PENDING':
        booking.delete()
        
        from carservice.utils import log_activity, get_client_ip, send_log
        ip = get_client_ip(request)
        log_activity(f"Booking cancelled by {request.user.username} (Booking ID: {booking_id}) from {ip}")
        send_log("BOOKING_CANCELLED", ip, request.user.username)
        
        messages.success(request, "Booking cancelled successfully.")
    else:
        from carservice.utils import log_activity, get_client_ip, send_log
        ip = get_client_ip(request)
        log_activity(f"Failed to cancel booking by {request.user.username} (Booking ID: {booking_id}, status: {booking.status}) from {ip}")
        send_log("BOOKING_CANCEL_FAILED", ip, request.user.username)
        
        messages.error(request, "Cannot cancel a booking that is already in progress or completed.")
        
    return redirect('customer_dashboard')
