from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from booking.models import Booking
from django.http import JsonResponse
from .forms import UserUpdateForm

@login_required
def mechanic_dashboard(request):
    if not hasattr(request.user, 'mechanic'):
        return redirect('login_redirect')
    
    mechanic = request.user.mechanic
    bookings = Booking.objects.filter(mechanic=mechanic).exclude(status__in=['DELIVERED', 'COMPLETED']).order_by('booking_date') # Active
    history = Booking.objects.filter(mechanic=mechanic, status__in=['DELIVERED', 'COMPLETED']).order_by('-booking_date')
    
    return render(request, 'mechanicpanel/dashboard.html', {
        'bookings': bookings,
        'history': history,
        'status_choices': Booking.STATUS_CHOICES
    })

@login_required
def update_booking_status(request, booking_id):
    if not hasattr(request.user, 'mechanic'):
         return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id, mechanic=request.user.mechanic)
        new_status = request.POST.get('status')
        if new_status and any(new_status == choice[0] for choice in Booking.STATUS_CHOICES):
            booking.status = new_status
            booking.save()
            return redirect('mechanic_dashboard')
            
    return redirect('mechanic_dashboard')

@login_required
def mechanic_profile(request):
    if not hasattr(request.user, 'mechanic'):
        return redirect('login_redirect')
        
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # m_form = MechanicUpdateForm(request.POST, instance=request.user.mechanic) # No fields yet
        if u_form.is_valid():
            u_form.save()
            # m_form.save()
            return redirect('mechanic_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        # m_form = MechanicUpdateForm(instance=request.user.mechanic)

    return render(request, 'mechanicpanel/profile.html', {
        'u_form': u_form,
        'mechanic': request.user.mechanic
    })
