# app/website/consumers.py
from channels.generic.websocket import JsonWebsocketConsumer
from django.template.loader import render_to_string
from .models import Message
from asgiref.sync import async_to_sync

class SocialNetworkConsumer(JsonWebsocketConsumer):

    room_name = 'broadcast'
    max_messages_per_page = 5

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
            case 'list messages':
                # Send messages to all clients
                self.send_list_messages(data['page'])

    def send_list_messages(self, page=1):
        start_pager = self.max_messages_per_page * (page - 1)
        end_pager = start_pager + self.max_messages_per_page
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {
                'type': 'send.html',
                'selector': '#messages__list',
                'html': render_to_string('components/_list-messages.html',
                                         {
                                             'messages': Message.objects.order_by('-created_at')[start_pager:end_pager],
                                         })
            }
        )

    def send_html(self, event):
        data = {
            'selector': event['selector'],
            'html': event['html'],
        }
        self.send_json(data)