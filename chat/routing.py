from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:sender_id>/<int:recipient_id>/', ChatConsumer.as_asgi()),
]
