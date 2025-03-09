from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from ticker.consumers import TickerConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        re_path(r'ws/tickers/$', TickerConsumer.as_asgi()),
    ]),
})