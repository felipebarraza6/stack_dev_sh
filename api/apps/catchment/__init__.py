"""
Catchment App
"""

default_app_config = 'api.apps.catchment.apps.CatchmentAppConfig'

# Los modelos se descubren automáticamente por Django
# No importar modelos aquí para evitar AppRegistryNotReady

# Importar serializers
# from .serializers.serializers import (
#     CatchmentPointSerializer, 
#     CatchmentPointProcessingConfigSerializer,
#     NotificationsCatchmentSerializer
# )

__all__ = [
    # 'CatchmentPoint',
    # 'CatchmentPointProcessingConfig',
    # 'CatchmentPointNotification',
    # 'CatchmentPointSerializer',
    # 'CatchmentPointProcessingConfigSerializer',
    # 'NotificationsCatchmentSerializer',
] 