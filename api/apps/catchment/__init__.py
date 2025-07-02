"""
App de Puntos de Captación
"""

default_app_config = 'api.apps.catchment.apps.CatchmentConfig'

# Importar modelos
from .models.models import CatchmentPoint, CatchmentPointProcessingConfig, NotificationsCatchment

# Importar serializers
from .serializers.serializers import (
    CatchmentPointSerializer, 
    CatchmentPointProcessingConfigSerializer,
    NotificationsCatchmentSerializer
)

__all__ = [
    'CatchmentPoint',
    'CatchmentPointProcessingConfig',
    'NotificationsCatchment',
    'CatchmentPointSerializer',
    'CatchmentPointProcessingConfigSerializer',
    'NotificationsCatchmentSerializer',
] 