from rest_framework.decorators import api_view,permission_classes
from .permissions import IsDriver, IsAvailableDriver
from rest_framework.permissions import IsAuthenticated
from auth_user.utils import create_response
from rest_framework import status 
from django.contrib.auth import get_user_model
from .serializers import DriverProfileSerializer, VehicleDetailsSerializer
from .models import DriverProfile, VehicleDetails
from ride.models import Ride
from ride.serializers import RideSerializer
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db import transaction

User=get_user_model()

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def driverRegister(request):
    """
driverRegister
Registers a user as a driver.

Sample Request:
POST /driver/register
{
    "user": "user@example.com"
}

Sample Response (Success):
{
    "success": true,
    "message": "Registered successfully.",
    "data": {
        ...driver profile data...
    }
}

Sample Response (Failure):
{
    "success": false,
    "error": "User not found. Try after registering."
}
"""
    user=request.user
    if user.is_driver:
        return create_response(False, {"error": "User is already a driver."}, status=status.HTTP_400_BAD_REQUEST)
    driver_profile=DriverProfile.objects.create(user=user)
    user.is_driver=True
    if user.is_rider:
        user.is_rider=False
    user.save()
    data=DriverProfileSerializer(driver_profile)
    return create_response(True, {"message": "Registered successfully.", "data": data.data}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([IsDriver])

def vehicleRegistration(request):
    """
vehicleRegistration
Registers a vehicle for the authenticated driver.

    Sample Request:
    POST /driver/vehicle/register
    {
        "vehicle": {
            "vehicle_type": "car",
            "vehicle_number": "ABC123",
            "make": "Toyota",
            "model": "Camry",
            "color": "Blue",
        }
    }
    

Sample Response (Success):
{
    "success": true,
    "message": "Vehicle registered successfully.",
    "data": {
        ...vehicle data...
    }
}

Sample Response (Failure):
{
    "success": false,
    "error": "Invalid vehicle data.",
    "details": { ...serializer errors... }
}
"""
    user=request.user
    vehicle_data = request.data.get('vehicle')
    vehicle_data['driver'] = DriverProfile.objects.get(user=user).id
    vehicle_serializer = VehicleDetailsSerializer(data=vehicle_data)
    if vehicle_serializer.is_valid():
        vehicle = vehicle_serializer.save()
        return create_response(True, {"message": "Vehicle registered successfully.", "data": vehicle_serializer.data}, status=status.HTTP_201_CREATED)
    return create_response(False, {"error": "Invalid vehicle data.", "details": vehicle_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsDriver])

def toggleAvailability(request):
    """
toggleAvailability
Toggles the driver's availability status and updates location if available.

Sample Request:
POST /driver/toggle-availability
{
    "lng": 78.123,
    "lat": 17.456
}

Sample Response (Success):
{
    "success": true
}

Sample Response (Failure):
{
    "success": false,
    "message": "No driver exists"
}
"""
    user=request.user
    if not user.is_driver:
        return create_response(False,{'message':'No driver exists'},status=status.HTTP_404_NOT_FOUND)
    
    driver=DriverProfile.objects.get(user=user)
    if driver.is_available:
        driver.is_available=False
    else:
        driver.is_available=True
        loc=Point(float(request.data.get('lng')),float(request.data.get('lat')),srid=4326)
        print(loc)
        driver.location=loc
    driver.save()
    return create_response(True,{},status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsDriver])

def updateDriverLocation(request):
    """
updateDriverLocation
Updates the driver's current location.

Sample Request:
POST /driver/update-location
{
    "location": {
        "lng": 78.123,
        "lat": 17.456
    }
}

Sample Response (Success):
{
    "success": true
}

Sample Response (Failure):
{
    "success": false,
    "message": "Location data is required"
}
"""
    user=request.user
    driver=DriverProfile.objects.get(user=user)
    location_data = request.data.get("location")
    if not location_data:
        return create_response(False,{'message':'Location data is required'},status=status.HTTP_400_BAD_REQUEST)
    driver.location = Point(float(location_data["lng"]), float(location_data["lat"]), srid=4326)
    driver.save()
    return create_response(True,{},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsDriver])

def rideRequests(request):
    """
rideRequests
Fetches ride requests matching the driver's vehicle type.

Sample Request:
GET /driver/ride-requests

Sample Response (Success):
{
    "success": true,
    "rides": [
        ...list of ride objects...
    ]
}

Sample Response (Failure):
{
    "success": false,
    "message": "No vehicle found for the driver"
}
"""
    user=request.user
    driver=DriverProfile.objects.get(user=user)
    try:
        vehicle=VehicleDetails.objects.get(driver=driver)
    except VehicleDetails.DoesNotExist:
        return create_response(False,{'message':'No vehicle found for the driver'},status=status.HTTP_404_NOT_FOUND)
    rides=Ride.objects.filter(status='requested',type_of_vehicle=vehicle.vehicle_type,pickup_location__distance_lte=(driver.location,D(km=5))).order_by('-created_at')
    data=RideSerializer(rides,many=True)
    return create_response(True,{'rides':data.data},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsDriver, IsAvailableDriver])
def acceptRide(request):
    """"""
    user=request.user
    driver_profile=DriverProfile.objects.get(user=user)
    ride_id=request.data.get('ride_id')
    if not ride_id:
        return create_response(False,{"messsage":"Ride details are required"},status=status.HTTP_400_BAD_REQUEST)
    try:
        ride=Ride.objects.get(id=ride_id)
        if ride.driver:
            raise Exception("Already Driver was assigned")
        with transaction.atomic():
            ride.driver=driver_profile
            ride.status="in_progress"
            ride.save()
        return create_response(True,{"message":"Accepted Successfully","updated":f'{timezone.LocalTimezone()}'},status=status.HTTP_202_ACCEPTED)
    except Ride.DoesNotExist:
        return create_response(False,{"message":"Not exists"},status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return create_response(False,{"message":str(e)},status=status.HTTP_404_NOT_FOUND)
