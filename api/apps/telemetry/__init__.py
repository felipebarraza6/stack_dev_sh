"""
App de Telemetría - Sistema Modular de Captación de Datos
"""

default_app_config = 'api.apps.telemetry.apps.TelemetryConfig'

# Importar modelos principales
from .models.models import TelemetryData
from .models.models_schemas import TelemetrySchema, TelemetryGroup, TelemetrySchemaMapping, TelemetrySchemaProcessor

# Importar serializers
from .serializers.serializers import TelemetryDataSerializer
from .serializers.serializers_schemas import TelemetrySchemaSerializer

# Importar vistas
from .views.views import TelemetryViewSet

# Importar procesadores
from .processors.processor import TelemetryProcessor
from .processors.dga_processor import DgaQueueProcessor
from .processors.schema_processor import SchemaProcessor

# Importar proveedores
from .providers.providers import ProviderManager

# Importar configuración
from .config.config import TelemetryConfig
from .config.metrics import TelemetryMetrics

__all__ = [
    'TelemetryData',
    'TelemetrySchema',
    'TelemetryGroup',
    'TelemetrySchemaMapping',
    'TelemetrySchemaProcessor',
    'TelemetryDataSerializer',
    'TelemetrySchemaSerializer',
    'TelemetryViewSet',
    'TelemetryProcessor',
    'DgaQueueProcessor',
    'SchemaProcessor',
    'ProviderManager',
    'TelemetryConfig',
    'TelemetryMetrics',
] 