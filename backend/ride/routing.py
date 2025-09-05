from django.urls import re_path
from .consumer import DriverConsumer

websocket_urlpatterns = [
    re_path(r'ws/driver/(?P<driver_id>\d+)/$', DriverConsumer.as_asgi()),
]