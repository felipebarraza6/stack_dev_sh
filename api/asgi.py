"""
ASGI config for api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Configurar el entorno por defecto si no está definido
if 'DJANGO_ENV' not in os.environ:
    os.environ.setdefault('DJANGO_ENV', 'production')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

application = get_asgi_application()
