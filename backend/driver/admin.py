from django.contrib import admin
from .models import DriverProfile, VehicleDetails
# Register your models here.
@admin.register(DriverProfile)
class driverProfileAdmin(admin.ModelAdmin):
    list_display=['id','user','is_verified']

@admin.register(VehicleDetails)
class vehicleDetailsAdmin(admin.ModelAdmin):
    list_display=['id','driver','vehicle_type','vehicle_number']