"""
ASGI config for anime_video_converter project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import anime_video_converter.routing  # Make sure to import your app's routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anime_video_converter.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            anime_video_converter.routing.websocket_urlpatterns
        )
    ),
})
