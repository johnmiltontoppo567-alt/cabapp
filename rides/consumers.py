import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ride_id = self.scope['url_route']['kwargs']['ride_id']
        self.ride_group_name = f'ride_{self.ride_id}'

        await self.channel_layer.group_add(
            self.ride_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.ride_group_name,
            self.channel_name
        )

    async def ride_update(self, event):
        await self.send(text_data=json.dumps(event))

class DriverConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # All drivers join this group to hear about new pending rides
        self.group_name = 'drivers'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def ride_available(self, event):
        # Notify driver that a new ride is available
        await self.send(text_data=json.dumps(event))
