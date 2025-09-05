from django.urls import path
from .views import nearbyDrivers,requestRide
urlpatterns=[
    path('nearby-drivers/', nearbyDrivers, name='nearby-drivers'),
    path('request-ride/', requestRide, name='request-ride')
]