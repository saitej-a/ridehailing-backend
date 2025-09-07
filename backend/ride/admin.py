from django.contrib import admin

# Register your models here.
from .models import Ride
@admin.register(Ride)
class Rideadmin(admin.ModelAdmin):
    list_display=('id','driver','rider','status','actual_fare')
