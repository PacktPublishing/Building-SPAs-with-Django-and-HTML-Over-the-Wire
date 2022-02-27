# social_network/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from app.website.consumers import ExampleConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application(),
    # WebSocket handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r"^ws/social-network/$", ExampleConsumer.as_asgi()),
        ])
    ),
})