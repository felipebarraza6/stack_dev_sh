"""
Configuración de Django REST Framework para Desarrollo
Configuración más permisiva para facilitar el desarrollo
"""
from .base import REST_FRAMEWORK

# Configuración para desarrollo
REST_FRAMEWORK_DEV = REST_FRAMEWORK.copy()

# Agregar renderer para desarrollo (interfaz web de DRF)
REST_FRAMEWORK_DEV['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',  # Interfaz web para desarrollo
]

# Deshabilitar throttling en desarrollo para facilitar testing
REST_FRAMEWORK_DEV['DEFAULT_THROTTLE_CLASSES'] = []

# Configuración más permisiva para desarrollo
REST_FRAMEWORK_DEV.update({
    # Logging más detallado
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    
    # Configuración de debugging
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    
    # Permitir más tipos de contenido en desarrollo
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.FileUploadParser',
    ],
    
    # Configuración de caché más corta en desarrollo
    'DEFAULT_CACHE_TIMEOUT': 60,  # 1 minuto en desarrollo
    
    # Configuración de paginación más permisiva
    'PAGE_SIZE': 10,  # Más elementos por defecto en desarrollo
})

# Configuración específica para desarrollo
DEV_CONFIG = {
    'DEBUG': True,
    'SHOW_DEBUG_TOOLBAR': True,
    'ENABLE_PROFILING': True,
    'LOG_LEVEL': 'DEBUG',
    'ENABLE_SQL_LOGGING': True,
} 