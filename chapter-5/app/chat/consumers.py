# app/chat/consumers.py
from channels.generic.websocket import JsonWebsocketConsumer
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from channels.auth import login, logout
from django.contrib.auth.models import User
from .models import Client, Room


class ExampleConsumer(JsonWebsocketConsumer):

    # At startup delete all clients
    Client.objects.all().delete()

    def connect(self):
        """Event when client connects"""
        # Accept the connection
        self.accept()
        # Gets a random user not logged in
        user = User.objects.exclude(
            id__in=Client.objects.all().values('user')
        ).order_by('?').first()
        # Login
        login(self.scope, user)
        # Saves the new client
        client = Client.objects.create(user=user, channel_name=self.channel_name)
        # Assign the group #hi, the first group that will be displayed when you enter
        self.add_client_to_group(client, '#hi')


    def disconnect(self, close_code):
        """Event when client disconnects"""
        # Logout user
        logout(self.scope, self.user)
        # Remove the client from the current group
        self.remove_client_from_current_group(Client.objects.get(user=self.user))
        # Delete the client
        Client.objects.filter(user=self.user).delete()


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
            case 'Change group':
                pass
            case 'New message':
                pass


    def send_html(self, event):
        """Event: Send html to client"""
        data = {
            'selector': event['selector'],
            'html': event['html'],
        }
        self.send_json(data)


    def send_hello(self):
        """Send list of messages to client"""
        # Render HTML and send to client
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {
                'type': 'send.html', # Run 'send_html()' method
                'selector': '#main',
                'html': render_to_string("components/_login.html", {})
            }
        )

    def add_client_to_group(self, client, group_name, is_group=False):
        """Add customer to a group within Channels and save the reference in the Room model."""
        self.remove_client_from_current_group(client)
        room = Room.objects.get_or_create(name=group_name, is_group=is_group)
        room.client_set.add(client)
        async_to_sync(self.channel_layer.group_add)(room.name, self.channel_name)


    def remove_client_from_current_group(self, client):
        """Remove client from current group"""
        # Get the current group
        room = Room.objects.get(client_set=client)
        # Remove the client from the group
        async_to_sync(self.channel_layer.group_discard)(room.name, self.channel_name)
        # Delete the client
        room.client_set.remove(client)
        # If the group is empty, delete it
        if not room.client_set.all():
            room.delete()
