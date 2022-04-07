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
        # Display the username
        self.send_html(
            {
                "selector": "#logged-user",
                "html": self.scope["user"].username,
            }
        )
        # Register the client in the database to control who is connected.
        Client.objects.create(user=user, channel=self.channel_name)
        # Assign the group "hi", the first room that will be displayed when you enter
        self.add_client_to_room("hi", True)
        # List the messages
        self.list_room_messages()


    def disconnect(self, close_code):
        """Event when client disconnects"""
        # Remove the client from the current room
        self.remove_client_from_current_room()
        # Deregister the client
        Client.objects.get(channel=self.channel_name).delete()
        # Logout user
        logout(self.scope, self.scope["user"])


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
                if data["isGroup"]:
                    """isGroup is True: Add to a multi-user room: #hi, #python..."""
                    self.add_client_to_room(data["groupName"], data["isGroup"])
                else:
                    """isGroup is False: Add to private room with the target user and the current user."""
                    # Gets the user to whom you are going to speak
                    user_target = User.objects.filter(username=data["groupName"]).first()
                    # Search for rooms where both users match
                    room = Room.objects.filter(users_subscribed__in=[self.scope["user"]], is_group=False).intersection(Room.objects.filter(users_subscribed__in=[user_target], is_group=False)).first()
                    if room and user_target and room.users_subscribed.count() == 2:
                        # An existing group has been found where both target and current users are already talking.
                        # The current user subscribes
                        self.add_client_to_room(room.name)
                    else:
                        # Looking for a room where the target user is alone.
                        room = Room.objects.filter(
                            users_subscribed__in=[
                                user_target,
                            ],
                            is_group=False,
                        ).last()
                        if room and room.users_subscribed.count() == 1:
                            # There is a room, let's join.
                            self.add_client_to_room(room.name)
                        else:
                            # We have not found any room where the target user is alone, we create a new room.
                            self.add_client_to_room()
                # We inform the visitor in which room this
                self.send_room_name()
            case "New message":
                # We received a new message to save
                self.save_message(data["message"])
        # Send the list of messages from the room
        self.list_room_messages()


    def send_html(self, event):
        """Event: Send html to client"""
        data = {
            "selector": event["selector"],
            "html": event["html"],
        }
        self.send_json(data)


    def list_room_messages(self):
        """List all messages from a group"""
        room_name = self.get_name_room_active()
        # Get the room
        room = Room.objects.get(name=room_name)
        # Get all messages from the room
        messages = Message.objects.filter(room=room).order_by("created_at")
        # Render HTML and send to client
        async_to_sync(self.channel_layer.group_send)(
            room_name, {
                "type": "send.html", # Run "send_html()" method
                "selector": "#messages-list",
                "html": render_to_string("components/_list_messages.html", {"messages": messages})
            }
        )

    def send_room_name(self):
        """Send the room name to the client"""
        room_name = self.get_name_room_active()
        room = Room.objects.get(name=room_name)
        data = {
            "selector": "#group-name",
            # Concadena # if it is a group for aesthetic reasons
            "html": ("#" if room.is_group else "") + room_name,
        }
        self.send_json(data)


    def save_message(self, text):
        """Save a message in the database"""
        # Get the room
        room = Room.objects.get(name=self.get_name_room_active())
        # Save message
        Message.objects.create(
            user=self.scope["user"],
            room=room,
            text=text,
        )


    def add_client_to_room(self, room_name=None, is_group=False):
        """Add customer to a room within Channels and save the reference in the Room model."""
        # Get the user client
        client = Client.objects.get(user=self.scope["user"])
        # Remove the client from the previous room
        self.remove_client_from_current_room()
        # Get or create room
        room, created = Room.objects.get_or_create(name=room_name, is_group=is_group)
        # If it has no name, it is assigned "private_{id}"
        # For example, if the id is 1, it shall be "private_1".
        if not room.name:
            room.name = f"private_{room.id}"
            room.save()
        room.clients_active.add(client)
        room.users_subscribed.add(client.user)
        room.save()
        # Add client to room
        async_to_sync(self.channel_layer.group_add)(room.name, self.channel_name)
        # Send the group name to the client
        self.send_room_name()


    def get_name_room_active(self):
        """Get the name of the group from login user"""
        room = Room.objects.filter(clients_active__user_id=self.scope["user"].id).first()
        return room.name

    def remove_client_from_current_room(self):
        """Remove client from current group"""
        client = Client.objects.get(user=self.scope["user"])
        # Get the current group
        rooms = Room.objects.filter(clients_active__in=[client])
        for room in rooms:
            # Remove the client from the group
            async_to_sync(self.channel_layer.group_discard)(room.name, self.channel_name)
            # Remove the client from the Room model
            room.clients_active.remove(client)
            room.save()