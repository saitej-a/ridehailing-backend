from channels.generic.websocket import AsyncWebsocketConsumer
import json
class DriverConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.driver_id = self.scope['url_route']['kwargs']['driver_id']
        self.room_group_name = f'driver_{self.driver_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def notify_ride(self, event):
        # print(event)
        ride_data = event['data']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'ride': ride_data
        }))