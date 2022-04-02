# app/chat/consumers.py
from channels.generic.websocket import JsonWebsocketConsumer
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from channels.auth import login, logout
from django.contrib.auth.models import User
from .models import Client, Room, Message


class ChatConsumer(JsonWebsocketConsumer):

    # At startup delete all clients
    Client.objects.all().delete()

    def connect(self):
        """Event when client connects"""
        # Accept the connection
        self.accept()
        # Gets a random user not logged in
        user = User.objects.exclude(
            id__in=Client.objects.all().values("user")
        ).order_by("?").first()
        # Login
        async_to_sync(login)(self.scope, user)
        self.scope["session"].save()
        # Saves the new client
        client = Client.objects.create(user=user, channel=self.channel_name)
        # Assign the group "hi", the first group that will be displayed when you enter
        self.add_client_to_group("hi")


    def disconnect(self, close_code):
        """Event when client disconnects"""
        # Logout user
        logout(self.scope, self.scope["user"])
        # Remove the client from the current group
        self.remove_client_from_current_group(Client.objects.get(user=self.scope["user"]))
        # Delete the client
        Client.objects.filter(user=self.scope["user"]).delete()


    def receive_json(self, data_received):
        """
            Event when data is received
            All information will arrive in 2 variables:
            "action", with the action to be taken
            "data" with the information
        """
        # Get the data
        data = data_received["data"]
        # Depending on the action we will do one task or another.
        match data_received["action"]:
            case "Change group":
                self.add_client_to_group(data["group_name"], data["is_group"])
                self.list_group_messages(data["group_name"])
            case "New message":
                self.save_message(data["message"], data["group_name"])
                self.list_group_messages(data["group_name"])


    def send_html(self, event):
        """Event: Send html to client"""
        data = {
            "selector": event["selector"],
            "html": event["html"],
        }
        self.send_json(data)


    def list_group_messages(self, group_name):
        """List all messages from a group"""
        # Get the room
        room = Room.objects.get(name=group_name)
        # Get all messages from the room
        messages = Message.objects.filter(room=room)
        # Render HTML and send to client
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {
                "type": "send.html", # Run "send_html()" method
                "selector": "#main",
                "html": render_to_string("components/_list_messages.html.html", {"messages": messages})
            }
        )


    def save_message(self, message, group_name):
        """Save a message in the database"""
        # Get the room
        room = Room.objects.get(name=group_name)
        # Save message
        Message.objects.create(room=room, message=message)


    def add_client_to_group(self, group_name, user=None, is_group=False):
        """Add customer to a group within Channels and save the reference in the Room model."""
        # Get the user client
        client = Client.objects.get(user_id=user.id if user else self.scope["user"].id)
        self.remove_client_from_current_group(client)
        Room.objects.get_or_create(name=group_name, is_group=is_group)
        # Get o create room
        room = Room.objects.get(name=group_name)
        room.client.add(client)
        room.save()
        # Add client to group
        async_to_sync(self.channel_layer.group_add)(room.name, self.channel_name)


    def remove_client_from_current_group(self, client):
        """Remove client from current group"""
        # Get the current group
        room = Room.objects.filter(client__in=[client]).first()
        if room:
            # Remove the client from the group
            async_to_sync(self.channel_layer.group_discard)(room.name, self.channel_name)
            # Remove the client from the Room model
            room.client.remove(client)
            room.save()
            # If the group is empty, delete it
            if not room.client.all():
                room.delete()
