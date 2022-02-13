# hello_world/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from app.simple_app.consumers import EchoConsumer, BingoConsumer, BMIConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_world.settings')

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application(),
    # WebSocket handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r"^ws/echo/$", EchoConsumer.as_asgi()),
            re_path(r"^ws/bingo/$", BingoConsumer.as_asgi()),
            re_path(r"^ws/bmi/$", BMIConsumer.as_asgi()),
        ])
    ),
})