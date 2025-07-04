"""
Users App
"""

default_app_config = 'api.apps.users.apps.UsersAppConfig'

# Los modelos se descubren automáticamente por Django
# No importar modelos aquí para evitar AppRegistryNotReady

# Importar serializers
# from .serializers.users import UserSerializer

__all__ = [
    # 'User',
    # 'UserSerializer',
] 