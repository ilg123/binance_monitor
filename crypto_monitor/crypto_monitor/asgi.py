import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from ticker.consumers import TickerConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto_monitor.settings')
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/tickers/$', TickerConsumer.as_asgi()),
        ])
    ),
})