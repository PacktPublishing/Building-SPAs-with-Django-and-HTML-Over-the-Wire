# app/website/consumers.py
from channels.generic.websocket import JsonWebsocketConsumer
from django.template.loader import render_to_string


class SocialNetworkConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        message = {
            "action": "connected",
            "html": render_to_string("components/_welcome.html", {}),
        }
        self.send_json(content=message)

    def disconnect(self, close_code):
        """Event when client disconnects"""
        pass

    def receive_json(self, data):
        """Event when data is received"""
        pass
