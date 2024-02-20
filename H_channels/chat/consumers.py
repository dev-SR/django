import datetime
from pprint import pprint

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.template.loader import render_to_string


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # accept connection
        await self.accept()
        print("*" * 50)
        print("You are connected to websocket")
        # pprint(self.scope)
        self.user = self.scope["user"]
        print(self.user.username)

    # receive htmx
    async def receive_json(self, data):
        print("*" * 50)
        print("WebSocket received data:")
        pprint(data)
        try:
            chat_message = data.get('chat_message')
            print(chat_message)
            if not chat_message:
                # Handle case where chat message is not present in data
                return

            # Get current tim
            chat_message_time = datetime.datetime.now()

            # Render template with message and time
            html = render_to_string("chat/partials/ws_response.html",
                                    {'message': chat_message,
                                     'time': chat_message_time,
                                     "user": self.user
                                     })

            # Send HTML response via WebSocket
            await self.send(text_data=html)

        except Exception as e:
            # Log any errors for debugging
            print(f"Error occurred: {e}")
