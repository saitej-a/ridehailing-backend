from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def notify_nearby_drivers(ride, nearby_drivers):
    channel_layer = get_channel_layer()
    for driver in nearby_drivers:
        async_to_sync(channel_layer.group_send)(
            f"driver_{driver.id}",
            {
                "type": "notify_ride",
                "data": {
                    "ride_id": ride.id,
                    "pickup": ride.pickup_location.coords,
                    "dropoff": ride.dropoff_location.coords,
                },
            }
        )
