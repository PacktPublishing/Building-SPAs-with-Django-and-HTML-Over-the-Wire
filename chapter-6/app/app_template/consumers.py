# app/app_template/consumers.py
from channels.generic.websocket import JsonWebsocketConsumer
from django.template.loader import render_to_string
from django.urls import reverse
from .forms import LoginForm, SignupForm


class ExampleConsumer(JsonWebsocketConsumer):

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
            "action", with the action to be taken
            "data" with the information
        """
        # Get the data
        data = data_received["data"]
        # Depending on the action we will do one task or another.
        match data_received["action"]:
            case "Change page":
                self.send_page(data["page"])


    def send_html(self, event):
        """Event: Send html to client"""
        data = {
            "selector": event["selector"],
            "html": event["html"],
            "append": event["append"],
            "url": event["url"] if "url" in event else "",
        }
        self.send_json(data)


    def send_page(self, page):
        """Render HTML and send page to client"""
        data = {}
        match page:
            case "login":
                data = {"form": LoginForm()}
            case "signup":
                data = {"form": SignupForm()}

        self.send_html({
            "selector": "#main",
            "html": render_to_string(f"pages/{page}.html", data),
            "append": False,
            "url": reverse(page)
            ,
        })