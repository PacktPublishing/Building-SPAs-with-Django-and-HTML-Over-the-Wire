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

    def disconnect(self, close_code):
        """Event when client disconnects"""
        pass

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
            case 'text in capital letters':
                self.send_uppercase(data)


    def send_uppercase(self, data):
        """Event: Send html to client"""
        self.send_json( {
                'type': 'send.html', # Run 'send_html()' method
                'selector': '#results',
                'html': data["text"].upper(),
            })