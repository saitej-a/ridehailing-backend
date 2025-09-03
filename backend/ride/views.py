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
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def nearbyDrivers(request):
    user_location = request.data.get("location")
    if not user_location:
        return create_response(False, "Location is required", status=400)

    user_point = Point(float(user_location["lng"]), float(user_location["lat"]), srid=4326)

    nearby_drivers = DriverProfile.objects.filter(is_available=True, location__distance_lte=(user_point, D(km=5))).annotate(distance=Distance('location', user_point)).order_by('distance')
    drivers_data = [{
        "id": driver.id,
        "name": driver.user.full_name,
        "distance_km": driver.distance.km
    } for driver in nearby_drivers]
    return create_response(True,drivers_data,status=status.HTTP_200_OK)