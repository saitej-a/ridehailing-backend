from django.urls import path
from .views import *
urlpatterns=[
    path('register/',registerUser),
    path('register/sendemailotp/',generateOTP),
    path('register/verifyemail/',verifyOTP),
]