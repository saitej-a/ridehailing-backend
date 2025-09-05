from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Ride
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from auth_user.utils import create_response
from driver.models import DriverProfile
from rest_framework import status
