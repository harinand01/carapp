from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomerSignUpForm

def is_admin(user):
    return user.is_authenticated and user.is_superuser

def register(request):
    if request.user.is_authenticated:
        return redirect('login_redirect')
        
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            from carservice.utils import log_activity, get_client_ip
            ip = get_client_ip(request)
            log_activity(f"User registration success (user: {user.username}) from {ip}")
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('customer_dashboard')
    else:
        form = CustomerSignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_redirect(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if user.is_superuser or user.is_staff:
        return redirect('/admin/')
    elif hasattr(user, 'mechanic'):
        return redirect('mechanic_dashboard')
    elif hasattr(user, 'customer'):
        return redirect('customer_dashboard')
    else:
        return render(request, 'accounts/pending_setup.html')

def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='admin123'
        )
        return HttpResponse("Admin user created successfully!")
    return HttpResponse("Admin user already exists.")
