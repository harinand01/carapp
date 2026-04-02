from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vehicle
from booking.models import Booking
from .forms import VehicleForm, UserUpdateForm, CustomerUpdateForm

@login_required
def customer_dashboard(request):
    if not hasattr(request.user, 'customer'):
        return redirect('login_redirect')
    
    customer = request.user.customer
    bookings = Booking.objects.filter(customer=customer).order_by('-created_at')
    vehicles = Vehicle.objects.filter(customer=customer)
    
    return render(request, 'customer/dashboard.html', {
        'bookings': bookings,
        'vehicles': vehicles
    })

@login_required
def add_vehicle(request):
    if not hasattr(request.user, 'customer'):
        return redirect('login_redirect')

    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.customer = request.user.customer
            vehicle.save()
            messages.success(request, 'Vehicle added successfully!')
            return redirect('customer_dashboard')
    else:
        form = VehicleForm()
    return render(request, 'customer/add_vehicle.html', {'form': form})

@login_required
def vehicle_list(request):
    if not hasattr(request.user, 'customer'):
        return redirect('login_redirect')
    vehicles = Vehicle.objects.filter(customer=request.user.customer)
    return render(request, 'customer/vehicles.html', {'vehicles': vehicles})

@login_required
def profile(request):
    if not hasattr(request.user, 'customer'):
        return redirect('login_redirect')
        
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        c_form = CustomerUpdateForm(request.POST, instance=request.user.customer)
        if u_form.is_valid() and c_form.is_valid():
            u_form.save()
            c_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('customer_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        c_form = CustomerUpdateForm(instance=request.user.customer)

    return render(request, 'customer/profile.html', {
        'u_form': u_form,
        'c_form': c_form
    })

@login_required
def delete_vehicle(request, vehicle_id):
    if not hasattr(request.user, 'customer'):
        return redirect('login_redirect')
        
    from django.shortcuts import get_object_or_404
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, customer=request.user.customer)
    
    vehicle.delete()
    messages.success(request, "Vehicle removed successfully.")
    return redirect('customer_dashboard')
