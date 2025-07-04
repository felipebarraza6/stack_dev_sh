"""
Compliance App
"""

default_app_config = 'api.apps.compliance.apps.ComplianceConfig'

# Los modelos se descubren automáticamente por Django
# No importar modelos aquí para evitar AppRegistryNotReady

# Importar serializers
# from .serializers.serializers import (
#     ComplianceSourceSerializer, ComplianceConfigSerializer, 
#     ComplianceDataSerializer
# ) 