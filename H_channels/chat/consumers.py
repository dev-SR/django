# from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

import datetime
from pprint import pprint

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.template.loader import render_to_string
from chat.models import Conversation, Message
from django.contrib.auth import get_user_model
User = get_user_model()


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("*" * 50)
        print("You are connected to websocket")
        # pprint(self.scope)
        self.user = self.scope["user"]
        print(self.user.username)
        # extract conversation id from the scope
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        print(f"Conversation ID: {self.conversation_id}")
        self.conversation_group_name = f'chat_{self.conversation_id}'

        # Verify if user is part of the conversation
        is_participant = await self.check_participant()

        if not is_participant:
            await self.close()
            print("You are not part of this conversation")
            return

        # accept connection
        await self.accept()

        # Join conversation group
        await self.channel_layer.group_add(
            self.conversation_group_name,
            self.channel_name
        )  # adding the client/channel to the group

        print(f"User {self.user.username} has joined the conversation")

    @database_sync_to_async  # otherwsie it will raise an error: You cannot call this from an async context - use a thread or sync_to_async
    def check_participant(self):
        try:
            conversation = Conversation.objects.get(id=self.conversation_id)
            return self.user in conversation.participants.all()
        except Conversation.DoesNotExist:
            return False

    # receive htmx
    async def receive_json(self, data):
        print("*" * 50)
        print("WebSocket received data:")
        pprint(data)
        try:
            message_content = data.get('chat_message')
            print(message_content)
            if not message_content:
                # Handle case where chat message is not present in data
                return

            # Create and save message
            message = await self.create_message(message_content)

            # Broadcast message to conversation group
            await self.channel_layer.group_send(
                self.conversation_group_name,
                {
                    'type': 'chat_message',
                    'message': message.content,
                    'sender': message.sender.username,
                    'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                }
            )

        except Exception as e:
            # Log any errors for debugging
            print(f"Error occurred: {e}")

    @database_sync_to_async
    def create_message(self, content):
        return Message.objects.create(conversation_id=self.conversation_id, sender=self.user, content=content)

    async def chat_message(self, event):
        # Send message to WebSocket
        message_sender = event['sender']
        message_content = event['message']
        message_timestamp = datetime.datetime.fromisoformat(event['timestamp'])

        if message_sender == self.user.username:
            # Render template with message and time
            html = render_to_string("chat/partials/sender.html",
                                    {"message": {
                                        "content": message_content,
                                        "timestamp": message_timestamp}
                                     })

            # Send HTML response via WebSocket
            await self.send(text_data=html)
        else:
            # Render template with message and time
            html = render_to_string("chat/partials/receiver.html",
                                    {"message": {
                                        "content": message_content,
                                        "timestamp": message_timestamp}
                                     })

            # Send HTML response via WebSocket
            await self.send(text_data=html)

    async def disconnect(self, close_code):
        # Leave conversation group
        await self.channel_layer.group_discard(
            self.conversation_group_name,
            self.channel_name
        )
        print(f"User {self.user.username} has left the conversation")
