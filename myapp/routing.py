from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:room_path>/', consumers.ChatConsumer.as_asgi()),
]