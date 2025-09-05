from django.contrib.gis.db import models
from driver.models import DriverProfile
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your models here.
class Ride(models.Model):
    driver=models.ForeignKey(DriverProfile,on_delete=models.CASCADE,related_name='driver',null=True,blank=True)
    rider=models.ForeignKey(User,on_delete=models.CASCADE,related_name='rider')
    pickup_location=models.PointField(geography=True)
    dropoff_location=models.PointField(geography=True)
    status=models.CharField(max_length=20,choices=(
        ('requested','Requested'),
        ('in_progress','In Progress'),
        ('completed','Completed'),
        ('cancelled','Cancelled'),
    ))
    type_of_vehicle=models.CharField(max_length=20,choices=[
        ('bike','Bike'),
        ('auto','Auto'),
        ('car','Car'),
    ])
    estimated_fare=models.DecimalField(max_digits=10, decimal_places=2)
    actual_fare=models.DecimalField(max_digits=10, decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)