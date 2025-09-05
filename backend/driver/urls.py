from django.urls import path, include
from .views import toggleAvailability,updateDriverLocation, driverRegister, rideRequests, vehicleRegistration


urlpatterns =[
    path('toggle-availability/',toggleAvailability),
    path('update-location/',updateDriverLocation),
    path('register/', driverRegister),
    path('ride-requests/', rideRequests),
    path('vehicle-registration/', vehicleRegistration),
]