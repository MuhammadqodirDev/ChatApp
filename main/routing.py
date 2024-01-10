from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from main.consumers import ChatConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter(
        [
            path('ws/consumer/', ChatConsumer.as_asgi()),
        ]
    ),
})
