# app/simple_app/consumers.py
from channels.generic.websocket import WebsocketConsumer

class EchoConsumer(WebsocketConsumer):

    def connect(self):
        """Event when client connects"""

        # Informs client of successful connection
        self.accept()

        # Send message to client
        self.send(text_data="You are connected by WebSockets!")

    def disconnect(self, close_code):
        """Event when client disconnects"""
        pass

    def receive(self, text_data):
        """Event when data is received"""
        pass
