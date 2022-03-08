# app/website/consumers.py
from channels.generic.websocket import JsonWebsocketConsumer
from django.template.loader import render_to_string
from .models import Message
from asgiref.sync import async_to_sync
import math


class SocialNetworkConsumer(JsonWebsocketConsumer):

    room_name = 'broadcast'
    max_messages_per_page = 5

    def connect(self):
        """Event when client connects"""
        # Accept the connection
        self.accept()
        # Assign the Broadcast group
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        # Send you all the messages stored in the database.
        self.send_list_messages()

    def disconnect(self, close_code):
        """Event when client disconnects"""
        # Remove from the Broadcast group
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)

    def receive_json(self, data_received):
        """
            Event when data is received
            All information will arrive in 2 variables:
            'action', with the action to be taken
            'data' with the information
        """

        # Get the data
        data = data_received['data']
        # Depending on the action we will do one task or another.
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
            case 'delete message':
                # Delete message from database
                Message.objects.get(id=data['id']).delete()
                # Send messages to all clients
                self.send_list_messages()


    def send_html(self, event):
        """Event: Send html to client"""
        data = {
            'selector': event['selector'],
            'html': event['html'],
        }
        self.send_json(data)


    def send_list_messages(self, page=1):
        """Send list of messages to client"""
        # Filter messages to the current page
        start_pager = self.max_messages_per_page * (page - 1)
        end_pager = start_pager + self.max_messages_per_page
        messages = Message.objects.order_by('-created_at')
        messages_page = messages[start_pager:end_pager]
        # Render HTML and send to client
        total_pages = math.ceil(messages.count() / self.max_messages_per_page)
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {
                'type': 'send.html', # Run 'send_html()' method
                'selector': '#messages__list',
                'html': render_to_string('components/_list-messages.html', {
                    'messages': messages_page,
                    'page': page,
                    'total_pages': total_pages,
                }) 
            }
        )
