from rest_framework.decorators import api_view,permission_classes
from .permissions import IsDriver
from rest_framework.permissions import IsAuthenticated
from auth_user.utils import create_response
from rest_framework import status 
from django.contrib.auth import get_user_model
from .serializers import DriverProfileSerializer, VehicleDetailsSerializer
from .models import DriverProfile, VehicleDetails
from django.contrib.gis.geos import Point
User=get_user_model()

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def driverRegister(request):
    user_email=request.data.get('user')
    user=User.objects.filter(email=user_email).first()
    if not user:
        return create_response(False, {"error": "User not found. Try after registering."}, status=status.HTTP_404_NOT_FOUND)
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
    user=request.user
    vehicle_data = request.data.get('vehicle')
    vehicle_serializer = VehicleDetailsSerializer(data=vehicle_data)
    if vehicle_serializer.is_valid():
        vehicle = vehicle_serializer.save()
        user.vehicle=vehicle
        user.save()
        return create_response(True, {"message": "Vehicle registered successfully.", "data": data.data}, status=status.HTTP_201_CREATED)
    return create_response(False, {"error": "Invalid vehicle data.", "details": vehicle_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsDriver])
def toggleAvailability(request):
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
    user=request.user
    driver=DriverProfile.objects.get(user=user)
    location_data = request.data.get("location")
    if not location_data:
        return create_response(False,{'message':'Location data is required'},status=status.HTTP_400_BAD_REQUEST)
    driver.location = Point(float(location_data["lng"]), float(location_data["lat"]), srid=4326)
    driver.save()
    return create_response(True,{},status=status.HTTP_200_OK)
