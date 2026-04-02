from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('add-vehicle/', views.add_vehicle, name='add_vehicle'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('profile/', views.profile, name='customer_profile'),
    path('delete-vehicle/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
]
