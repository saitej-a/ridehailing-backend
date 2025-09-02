from django.urls import path, include
from .views import toggleAvailability
urlpatterns =[
    path('toggle-availability/',toggleAvailability)
]