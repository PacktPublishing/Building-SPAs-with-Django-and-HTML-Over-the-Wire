# app/app_template/consumers.py
from channels.generic.websocket import JsonWebsocketConsumer
import app.app_template.actions as actions


class ExampleConsumer(JsonWebsocketConsumer):

    def connect(self):
        """Event when client connects"""
        # Accept the connection
        self.user = self.scope["user"]
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
                actions.send_page(self, data["page"])
            case "Signup":
                actions.signup(self, data)
            case "Login":
                actions.login(self, data)
            case "Logout":
                actions.logout(self)
            case "Add lap":
                actions.add_lap(self)


    def send_html(self, event):
        """Event: Send html to client"""
        data = {
            "selector": event["selector"],
            "html": event["html"],
            "append": "append" in event and event["append"],
            "url": event["url"] if "url" in event else "",
        }
        self.send_json(data)