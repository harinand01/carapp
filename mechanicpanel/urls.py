from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.mechanic_dashboard, name='mechanic_dashboard'),
    path('profile/', views.mechanic_profile, name='mechanic_profile'),
    path('update-status/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
]
