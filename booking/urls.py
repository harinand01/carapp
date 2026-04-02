from django.urls import path
from . import views

urlpatterns = [
    path('services/', views.service_list, name='service_list'),
    path('book/', views.book_service, name='book_service'),
    path('payment/<int:booking_id>/', views.payment_status, name='payment_status'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
