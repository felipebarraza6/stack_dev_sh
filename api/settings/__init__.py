"""
Configuración del proyecto SmartHydro
"""
import os

# Determinar el entorno basado en la variable de entorno DJANGO_SETTINGS_MODULE
# o usar development por defecto
environment = os.environ.get('DJANGO_ENV', 'development')

if environment == 'production':
    from .production import *
else:
    from .development import * 