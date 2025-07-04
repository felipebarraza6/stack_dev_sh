"""
Providers App
"""

default_app_config = 'api.apps.providers.apps.ProvidersAppConfig'

# Los modelos se descubren automáticamente por Django
# No importar modelos aquí para evitar AppRegistryNotReady

# Importar clientes
from .clients.mqtt_client import DynamicMQTTClient

__all__ = [
    'DynamicMQTTClient',
] 