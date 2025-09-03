from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User=get_user_model()

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # current_location_lat=models.FloatField(null=True,blank=True)
    # current_location_lng=models.FloatField(null=True,blank=True)
    location=models.PointField(geography=True,null=True,blank=True)
    is_available = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.full_name
class VehicleDetails(models.Model):
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE,related_name='vehicle_owner')
    vehicle_number = models.CharField(max_length=20, unique=True)
    make=models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    vehicle_type= models.TextField(choices=[
        ('car', 'Car'),
        ('bike', 'Bike'),
    ])
    def __str__(self):
        return self.vehicle_number