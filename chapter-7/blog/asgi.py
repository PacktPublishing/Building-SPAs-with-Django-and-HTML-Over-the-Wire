# blog/asgi.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
from django.conf import settings

django.setup()
from django.core.asgi import get_asgi_application
from channels.security.websocket import OriginValidator
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from app.website.consumers import BlogConsumer


application = ProtocolTypeRouter(
    {
        # Django's ASGI application to handle traditional HTTP requests
        "http": get_asgi_application(),
        # WebSocket handler
        "websocket": OriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    [
                        re_path(r"^ws/blog/$", BlogConsumer.as_asgi()),
                    ]
                )
            ),
            settings.ALLOWED_HOSTS,
        ),
    }
)
