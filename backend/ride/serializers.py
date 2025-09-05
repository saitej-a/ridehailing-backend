from rest_framework.serializers import ModelSerializer
from .models import Ride

class RideSerializer(ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'