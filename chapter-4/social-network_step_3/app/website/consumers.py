# app/website/consumers.py
from channels.generic.websocket import JsonWebsocketConsumer
from django.template.loader import render_to_string
from .models import Message
from asgiref.sync import async_to_sync

class SocialNetworkConsumer(JsonWebsocketConsumer):

    room_name = 'broadcast'

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
                self.send_list_messages()


    def send_html(self, event):
        """Event: Send html to client"""
        data = {
            'selector': event['selector'],
            'html': event['html'],
        }
        self.send_json(data)


    def send_list_messages(self):
        """Send list of messages to client"""
        # Filter messages to the current page
        messages = Message.objects.order_by('-created_at')
        # Render HTML and send to client
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {
                'type': 'send.html', # Run 'send_html()' method
                'selector': '#messages__list',
                'html': render_to_string('components/_list-messages.html', { 'messages': messages})
            }
        )
