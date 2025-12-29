from django.urls import path
from .views import *

urlpatterns = [
    path("", ride_list, name="ride_list"),
    path("create/", ride_create, name="ride_create"),
    path("<int:ride_id>/", ride_detail, name="ride_detail"),
    path("<int:ride_id>/update/", ride_update, name="ride_update"),
    path("<int:ride_id>/delete/", ride_delete, name="ride_delete"),
    path('book/<int:ride_id>/', book_ride, name='book_ride'),
    path('bookings/', book_list, name='booking_list'),
]
