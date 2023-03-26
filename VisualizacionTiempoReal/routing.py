from django.urls import re_path
from . import consumers
websocket_urlpatterns = [
    # url conexion a socket 
    re_path(r'ws/socket-server/', consumers.VisualizacionTiempoRealConsumer.as_asgi())
]