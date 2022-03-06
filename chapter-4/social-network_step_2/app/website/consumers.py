# app/website/consumers.py
from channels.generic.websocket import JsonWebsocketConsumer
from django.template.loader import render_to_string
from .models import Message
from asgiref.sync import async_to_sync

class SocialNetworkConsumer(JsonWebsocketConsumer):

    room_name = 'broadcast'

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.send_list_messages()

    def disconnect(self, close_code):
        """Event when client disconnects"""
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)

    def receive_json(self, data_received):
        """Event when data is received"""
        data = data_received['data']
        match data_received['action']:
            case 'add message':
                # Add message to database
                Message.objects.create(
                    author=data['author'],
                    text=data['text'],
                )
                # Send messages to all clients
                self.send_list_messages()

    def send_list_messages(self):
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {
                'type': 'send.html',
                'selector': '#list-messages',
                'html': render_to_string('components/_list-messages.html', {'messages': Message.objects.all()})
            }
        )

    def send_html(self, event):
        data = {
            'selector': event['selector'],
            'html': event['html'],
        }
        self.send_json(data)