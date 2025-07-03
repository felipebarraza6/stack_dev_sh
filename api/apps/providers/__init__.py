"""
App de Providers
"""

default_app_config = 'api.apps.providers.apps.ProvidersAppConfig'

# No importar modelos ni serializers aquí para evitar ciclos de importación.

# from .models.models import (
#     Provider, MQTTBroker, DeviceToken, DataSchema, DataIngestionLog
# )

# Importar serializers
# from .serializers.serializers import (
#     ProviderSerializer, MQTTBrokerSerializer, DeviceTokenSerializer
# )

# Importar clientes
from .clients.mqtt_client import DynamicMQTTClient

# Importaciones tardías para evitar ciclos pero permitir acceso directo
def __getattr__(name):
    """Permitir acceso directo a modelos y serializers"""
    if name in ['Provider', 'ProviderSchemaMapping', 'MQTTBroker', 'DeviceToken', 'DataSchema', 'DataIngestionLog']:
        # Importar modelos
        from .models.providers.provider import Provider, ProviderSchemaMapping
        from .models.mqtt.broker import MQTTBroker
        from .models.tokens.device_token import DeviceToken
        from .models.schemas.data_schema import DataSchema
        from .models.logs.ingestion_log import DataIngestionLog
        
        models = {
            'Provider': Provider,
            'ProviderSchemaMapping': ProviderSchemaMapping,
            'MQTTBroker': MQTTBroker,
            'DeviceToken': DeviceToken,
            'DataSchema': DataSchema,
            'DataIngestionLog': DataIngestionLog,
        }
        return models[name]
    
    elif name in ['ProviderSerializer', 'ProviderDetailSerializer', 'MQTTBrokerSerializer', 'DeviceTokenSerializer', 'DataSchemaSerializer', 'DataIngestionLogSerializer']:
        # Importar serializers
        from .serializers.providers.provider import ProviderSerializer, ProviderDetailSerializer
        from .serializers.mqtt.broker import MQTTBrokerSerializer
        from .serializers.tokens.device_token import DeviceTokenSerializer
        from .serializers.schemas.data_schema import DataSchemaSerializer
        from .serializers.logs.ingestion_log import DataIngestionLogSerializer
        
        serializers = {
            'ProviderSerializer': ProviderSerializer,
            'ProviderDetailSerializer': ProviderDetailSerializer,
            'MQTTBrokerSerializer': MQTTBrokerSerializer,
            'DeviceTokenSerializer': DeviceTokenSerializer,
            'DataSchemaSerializer': DataSchemaSerializer,
            'DataIngestionLogSerializer': DataIngestionLogSerializer,
        }
        return serializers[name]
    
    raise AttributeError(f"module 'api.apps.providers' has no attribute '{name}'")

__all__ = [
    'DynamicMQTTClient',
] 