import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.layers import get_channel_layer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stregsystem.settings')


django_asgi_app = get_asgi_application()
channel_layer = get_channel_layer()

import cms.routing

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    #'websocket': AllowedHostsOriginValidator(
    #    AuthMiddlewareStack(
    #        URLRouter(
    #            cms.routing.websocket_urlpatterns
    #        )
    #    )
    #),
})
