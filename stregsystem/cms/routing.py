from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('update/<int:pk>', consumers.stregsystem_consumer.as_asgi()),
]
