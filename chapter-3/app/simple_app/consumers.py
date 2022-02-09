# app/simple_app/consumers.py
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
import time

class EchoConsumer(WebsocketConsumer):

    def connect(self):
        """Event when client connects"""

        # Informs client of successful connection
        self.accept()

        # Send message to client
        self.send(text_data="You are connected by WebSockets!")

    def disconnect(self, close_code):
        """Event when client disconnects"""
        self.run_time = False
        pass

    def receive(self, text_data):
        """Event when data is received"""

        # Send current the time
        self.send(text_data=str(datetime.now().strftime("%H:%M:%S")))