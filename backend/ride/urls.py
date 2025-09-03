from django.urls import path
from .views import nearbyDrivers
urlpatterns=[
    path('nearby-drivers/', nearbyDrivers, name='nearby-drivers'),
]