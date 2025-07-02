"""
App de Usuarios
"""

default_app_config = 'api.apps.users.apps.UsersConfig'

# Importar modelos
from .models.users import User

# Importar serializers
from .serializers.users import UserSerializer

__all__ = [
    'User',
    'UserSerializer',
] 