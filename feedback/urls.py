from django.urls import path
from . import views

urlpatterns = [
    path('give/<int:booking_id>/', views.give_feedback, name='give_feedback'),
]
