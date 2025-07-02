"""
Configuración base de Django REST Framework
Configuración común para todos los entornos
"""
from rest_framework import pagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class DynamicPageNumberPagination(pagination.PageNumberPagination):
    """
    Paginación dinámica que permite definir el tamaño de página en la consulta
    Por defecto: 10 elementos por página
    Máximo: 100 elementos por página
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'
    
    def get_paginated_response(self, data):
        """Respuesta personalizada con información de paginación"""
        return {
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            'page_info': {
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'page_size': self.get_page_size(self.request),
                'has_next': self.page.has_next(),
                'has_previous': self.page.has_previous(),
            }
        }


class CustomTokenAuthentication(TokenAuthentication):
    """
    Autenticación por token personalizada con mejor manejo de errores
    """
    def authenticate_credentials(self, key):
        """Autenticación con validación mejorada"""
        try:
            user, token = super().authenticate_credentials(key)
            return user, token
        except Exception as e:
            # Log del error para debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Error en autenticación por token: {str(e)}")
            raise


class CustomUserRateThrottle(UserRateThrottle):
    """
    Throttling personalizado para usuarios autenticados
    """
    rate = '1000/hour'  # 1000 requests por hora para usuarios autenticados


class CustomAnonRateThrottle(AnonRateThrottle):
    """
    Throttling personalizado para usuarios anónimos
    """
    rate = '100/hour'  # 100 requests por hora para usuarios anónimos


# Configuración base de DRF
REST_FRAMEWORK = {
    # Renderers
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    
    # Parsers
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
    
    # Autenticación
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.config.drf.base.CustomTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    
    # Permisos por defecto
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    # Paginación dinámica
    'DEFAULT_PAGINATION_CLASS': 'api.config.drf.base.DynamicPageNumberPagination',
    'PAGE_SIZE': 10,
    
    # Filtros y búsqueda
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    
    # Throttling (rate limiting)
    'DEFAULT_THROTTLE_CLASSES': [
        'api.config.drf.base.CustomUserRateThrottle',
        'api.config.drf.base.CustomAnonRateThrottle',
    ],
    
    # Throttling rates
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/hour',
        'anon': '100/hour',
        'burst': '60/minute',
    },
    
    # Configuración de versionado (opcional)
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    
    # Configuración de metadatos
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    
    # Configuración de excepciones
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    
    # Configuración de validación
    'NON_FIELD_ERRORS_KEY': 'error',
    
    # Configuración de formato de fecha
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATE_FORMAT': '%Y-%m-%d',
    'TIME_FORMAT': '%H:%M:%S',
    
    # Configuración de zona horaria
    'DATETIME_INPUT_FORMATS': [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f',
    ],
    
    # Configuración de serialización
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    
    # Configuración de caché
    'DEFAULT_CACHE_TIMEOUT': 300,  # 5 minutos
    
    # Configuración de compresión
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'rest_framework.negotiation.DefaultContentNegotiation',
} 