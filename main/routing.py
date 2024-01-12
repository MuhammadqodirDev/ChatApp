from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from main.consumers import ChatConsumer
from channels.auth import AuthMiddlewareStack


application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
            path('api/v1/ws/chat/', ChatConsumer.as_asgi()),
        ]
        )
    )
})
