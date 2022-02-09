# app/simple_app/consumers.py
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
import time
import threading

class EchoConsumer(WebsocketConsumer):

    def connect(self):
        """Event when client connects"""

        # Informs client of successful connection
        self.accept()

        # Send message to client
        self.send(text_data="You are connected by WebSockets!")

        # Send message to client every second
        def send_time(self):
            while True:
                # Send message to client
                self.send(text_data=str(datetime.now().strftime("%H:%M:%S")))
                # Sleep for 1 second
                time.sleep(1)
        threading.Thread(target=send_time, args=(self,)).start()

    def disconnect(self, close_code):
        """Event when client disconnects"""
        pass

    def receive(self, text_data):
        """Event when data is received"""
        pass