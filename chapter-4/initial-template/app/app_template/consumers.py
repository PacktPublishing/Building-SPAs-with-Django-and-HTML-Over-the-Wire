# app/app_template/consumers.py
from channels.generic.websocket import JsonWebsocketConsumer
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync


class ExampleConsumer(JsonWebsocketConsumer):

    room_name = 'broadcast'

    def connect(self):
        """Event when client connects"""
        # Accept the connection
        self.accept()
        # Assign the Broadcast group
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        # Send data
        self.send_hello()


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
            case 'example action':
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
                'html': render_to_string("components/_welcome.html", {})
            }
        )
