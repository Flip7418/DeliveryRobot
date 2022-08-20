from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/order-delivery/(?P<robot_title>\w+)/', consumers.OrderConsumer.as_asgi())
]
