# chat/routing.py
from django.conf.urls import url

from . import wsconsumers

websocket_urlpatterns = [
    url(r'^ws/(?P<room_name>[^/]+)/$', wsconsumers.ChatConsumer),
]