# from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async

from pprint import pprint

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.template.loader import render_to_string

from status.tasks import send_status_periodically


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("*" * 50)
        print("You are connected to websocket")
        self.group_name = 'status'
        # accept connection
        await self.accept()

        # Join conversation group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )  # adding the client/channel to the group

        # Send status to the client
        send_status_periodically.delay()

    #     await self.channel_layer.group_send(
    #         self.group_name,
    #         {
    #             'type': 'send_status',
    #             'status': 'RUNNING'
    #         }
    #     )

    async def send_status(self, event):
        # Send message to WebSocket
        status = event['status']
        print("Sending status to websocket...", status)
        html = render_to_string("status/partials/current_status.html", {"status": status})
        # Send HTML response via WebSocket
        await self.send(text_data=html)

    async def disconnect(self, close_code):
        # Leave conversation group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
