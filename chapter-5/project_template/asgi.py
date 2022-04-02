# project_template/asgi.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_template.settings")
django.setup()

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from app.chat.consumers import ChatConsumer


application = ProtocolTypeRouter(
    {
        # Django's ASGI application to handle traditional HTTP requests
        "http": get_asgi_application(),
        # WebSocket handler
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    re_path(r"^ws/example/$", ChatConsumer.as_asgi()),
                ]
            )
        ),
    }
)
