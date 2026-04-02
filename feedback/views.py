from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Feedback
from booking.models import Booking
from .forms import FeedbackForm

@login_required
def give_feedback(request, booking_id):
    if not hasattr(request.user, 'customer'):
        return redirect('login_redirect')
        
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user.customer)
    
    if booking.status not in ['COMPLETED', 'DELIVERED']:
        return redirect('customer_dashboard')
        
    # Check if feedback already exists
    if Feedback.objects.filter(booking=booking).exists():
        return redirect('customer_dashboard')

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.customer = request.user.customer
            feedback.booking = booking
            feedback.save()
            return redirect('customer_dashboard')
    else:
        form = FeedbackForm()
        
    return render(request, 'feedback/give_feedback.html', {'form': form, 'booking': booking})
