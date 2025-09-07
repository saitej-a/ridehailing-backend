from django.core.cache import cache
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from driver.models import DriverProfile
from django.contrib.gis.measure import D
import requests as req
import os
def estimateFare(distance, base_fare=20.0, per_km_rate=2.0, cost_per_minute=1.5, estimated_time=0,surge_multiplier=1.0,type_of_vehicle='bike'):
    """
    Estimate the fare for a ride based on distance.
    """
    print(type_of_vehicle)
    if distance < 0:
        raise ValueError("Distance cannot be negative")
    if type_of_vehicle == 'bike':
        base_fare=15.0
        per_km_rate=1.0
        cost_per_minute=1.0
    elif type_of_vehicle == 'car':
        base_fare=40
        per_km_rate=4.0
        cost_per_minute=4.0
    estimated_fare= (base_fare + ((float(distance) * per_km_rate) + (estimated_time * cost_per_minute)) * surge_multiplier)
    return estimated_fare

def calculateRideDuration(distance, average_speed=40, type_of_vehicle='bike'):
    """
    Calculate the estimated duration of a ride based on distance and average speed.
    """
    if distance < 0:
        raise ValueError("Distance cannot be negative")

    if type_of_vehicle == 'bike':
        average_speed = 40
    elif type_of_vehicle == 'car':
        average_speed = 60

    duration = distance / average_speed * 60  # Convert hours to minutes
    return duration
def calculateSurgeMultiplier(current_demand, normal_demand):
    """
    Calculate the surge multiplier based on current and normal demand.
    """
    if normal_demand == 0:
        raise ValueError("Normal demand cannot be zero")

    return current_demand / normal_demand
def calculateDistance(pickup_location, dropoff_location):
    """
    Calculate the distance between two geographic points.
    """
    if not pickup_location or not dropoff_location:
        raise ValueError("Both pickup and dropoff locations are required")
    return pickup_location.distance(dropoff_location) * 100

def nearbyDrivers_util(user_location_lat, user_location_lng):
    user_point = Point(float(user_location_lng), float(user_location_lat), srid=4326)
    nearby_drivers = DriverProfile.objects.filter(is_available=True, location__distance_lte=(user_point, D(km=5)),is_verified=True).annotate(distance=Distance('location', user_point)).order_by('distance')
    return nearby_drivers

def calculateRouteDistanceAndTime(pickup_location, dropoff_location) -> tuple:
    cache_key = f"route_{pickup_location}_{dropoff_location}"
    cached_result = cache.get(cache_key)
    if cached_result:
        print("from cached")
        return cached_result
    response = req.get(f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={pickup_location}&destinations={dropoff_location}&key={os.getenv('GOOGLE_MAPS_API_KEY')}")
    data = response.json()
    if data["status"] == "OK":
        print(data)
        route = data["rows"][0]["elements"][0]
        distance = round(route["distance"]["value"] / 1000)  # Distance in meters
        duration = round(route["duration"]["value"] / 60)  # Duration in seconds
        cache.set(cache_key, (distance, duration))
        return (distance, duration)
    else:
        raise ValueError("Error fetching route distance")