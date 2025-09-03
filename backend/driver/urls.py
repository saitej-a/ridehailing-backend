from django.urls import path, include
from .views import toggleAvailability,updateDriverLocation, driverRegister


urlpatterns =[
    path('toggle-availability/',toggleAvailability),
    path('update-location/',updateDriverLocation),
    path('register/', driverRegister)
]