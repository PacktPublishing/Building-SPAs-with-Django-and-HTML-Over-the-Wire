# app/simple_app/asgi.py
import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import app.simple_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_world.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            app.simple_app.routing.websocket_urlpatterns
        )
    ),
})