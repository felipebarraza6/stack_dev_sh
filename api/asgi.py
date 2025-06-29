"""
ASGI config for api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# Configurar el entorno por defecto si no está definido
if 'DJANGO_ENV' not in os.environ:
    os.environ.setdefault('DJANGO_ENV', 'production')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

# Importar las rutas de WebSocket después de configurar Django
from api.routing import websocket_urlpatterns

# Configuración ASGI para HTTP y WebSocket
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})
