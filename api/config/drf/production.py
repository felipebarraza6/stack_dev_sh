"""
Configuración de Django REST Framework para Producción
Configuración más estricta y segura para producción
"""
from .base import REST_FRAMEWORK

# Configuración para producción
REST_FRAMEWORK_PROD = REST_FRAMEWORK.copy()

# Configuración más estricta para producción
REST_FRAMEWORK_PROD.update({
    # Solo renderer JSON en producción (más seguro)
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    
    # Throttling más estricto en producción
    'DEFAULT_THROTTLE_RATES': {
        'user': '500/hour',  # Más restrictivo en producción
        'anon': '50/hour',   # Muy restrictivo para anónimos
        'burst': '30/minute', # Protección contra ataques
    },
    
    # Configuración de caché más larga en producción
    'DEFAULT_CACHE_TIMEOUT': 600,  # 10 minutos en producción
    
    # Configuración de paginación más conservadora
    'PAGE_SIZE': 10,  # Menos elementos por defecto en producción
    
    # Configuración de seguridad adicional
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.config.drf.base.CustomTokenAuthentication',
        # Removemos SessionAuthentication en producción para mayor seguridad
    ],
    
    # Configuración de excepciones más segura
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    
    # Configuración de metadatos mínima
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    
    # Configuración de parsers más restrictiva
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
    ],
})

# Configuración específica para producción
PROD_CONFIG = {
    'DEBUG': False,
    'SHOW_DEBUG_TOOLBAR': False,
    'ENABLE_PROFILING': False,
    'LOG_LEVEL': 'WARNING',
    'ENABLE_SQL_LOGGING': False,
    'SECURE_SSL_REDIRECT': True,
    'SESSION_COOKIE_SECURE': True,
    'CSRF_COOKIE_SECURE': True,
    'SECURE_BROWSER_XSS_FILTER': True,
    'SECURE_CONTENT_TYPE_NOSNIFF': True,
    'X_FRAME_OPTIONS': 'DENY',
} 