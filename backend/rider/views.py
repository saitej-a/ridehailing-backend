from auth_user.utils import create_response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.geos import Point
from driver.models import DriverProfile
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from ride.models import Ride
from .utils import estimateFare, calculateDistance, calculateRideDuration, nearbyDrivers_util, calculateRouteDistanceAndTime
from ride.serializers import RideSerializer
from ride.signals import notify_nearby_drivers
# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nearbyDrivers(request):
    user_location_lat = request.query_params.get("lat")
    user_location_lng = request.query_params.get("lng")
    if not user_location_lat or not user_location_lng:
        return create_response(False, "Location is required", status=400)

    nearby_drivers=nearbyDrivers_util(user_location_lat, user_location_lng)
    drivers_data = [{
        "id": driver.id,
        "name": driver.user.full_name,
        "distance_km": driver.distance.km
    } for driver in nearby_drivers]
    return create_response(True,drivers_data,status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def requestRide(request):
    user = request.user
    ride_data = request.data.get("ride")
    if not ride_data:
        return create_response(False, "Ride data is required", status=400)
    pickup_location = ride_data.get("pickup_location")
    dropoff_location = ride_data.get("dropoff_location")
    type_of_vehicle = ride_data.get("type_of_vehicle","bike")
    if not pickup_location or not dropoff_location:
        return create_response(False, "Pickup and dropoff locations are required", status=400)
    if 'lat' not in pickup_location or 'lng' not in pickup_location:
        return create_response(False, "Invalid pickup location", status=400)
    if 'lat' not in dropoff_location or 'lng' not in dropoff_location:
        return create_response(False, "Invalid dropoff location", status=400)
    
    
    try:
        distance, estimated_time = calculateRouteDistanceAndTime(f"{pickup_location.get('lat')},{pickup_location.get('lng')}",f"{dropoff_location.get('lat')},{dropoff_location.get('lng')}")
        estimated_fare = estimateFare(distance=distance, estimated_time=estimated_time, type_of_vehicle=type_of_vehicle)
    except Exception as e:
        return create_response(False, str(e), status=400)
    ride = Ride.objects.create(
        rider=user,
        pickup_location=Point(float(pickup_location.get("lng")), float(pickup_location.get("lat")), srid=4326),
        dropoff_location=Point(float(dropoff_location.get("lng")), float(dropoff_location.get("lat")), srid=4326),
        status='requested',
        estimated_fare=estimated_fare,
        actual_fare=estimated_fare,
        type_of_vehicle=type_of_vehicle
    )
    notify_nearby_drivers(ride,nearbyDrivers_util(pickup_location.get("lat"), pickup_location.get("lng")))
    return create_response(True, {"message":"Ride requested successfully","ride":RideSerializer(ride).data}, status=status.HTTP_201_CREATED)