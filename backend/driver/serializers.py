from rest_framework.serializers import ModelSerializer
from .models import DriverProfile, VehicleDetails

class DriverProfileSerializer(ModelSerializer):
    class Meta:
        model = DriverProfile
        fields = '__all__'

class VehicleDetailsSerializer(ModelSerializer):
    class Meta:
        model = VehicleDetails
        fields = '__all__'