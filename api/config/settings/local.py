"""
Configuración de Desarrollo Local
Solo modelo base, SQLite, sin telemetría - para testing de endpoints
"""
import sys
import os
from pathlib import Path
from .base import *

# =============================================================================
# CONFIGURACIÓN DE DESARROLLO LOCAL
# =============================================================================

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# =============================================================================
# BASE DE DATOS - SQLite para desarrollo local
# =============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'OPTIONS': {
            'timeout': 20,
        }
    }
}

# =============================================================================
# MODELO DE USUARIO PERSONALIZADO
# =============================================================================

AUTH_USER_MODEL = 'users.User'

# =============================================================================
# APPS ACTIVAS - Sistema completo habilitado
# =============================================================================

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'django_filters',
    'import_export',
    'drf_spectacular',  # Documentación automática
    
    # Local apps - Sistema completo
    'api.apps.core.apps.CoreConfig',           # ✅ Modelos base
    'api.apps.users.apps.UsersAppConfig',      # ✅ Usuarios
    'api.apps.providers.apps.ProvidersAppConfig',  # ✅ Proveedores de datos
    'api.apps.variables.apps.VariablesAppConfig',  # ✅ Variables
    'api.apps.catchment.apps.CatchmentAppConfig',  # ✅ Puntos de captación
    'api.apps.compliance.apps.ComplianceConfig',  # ✅ Cumplimiento
    'api.apps.telemetry.apps.TelemetryConfig',  # ✅ Telemetría
    'api.apps.frontend.apps.FrontendConfig',   # ✅ API Frontend
]

# =============================================================================
# CONFIGURACIÓN DRF - Simplificada para testing
# =============================================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# =============================================================================
# CACHE - Simple para desarrollo
# =============================================================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# =============================================================================
# LOGGING - Detallado para desarrollo
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/code/logs/django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'api': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# =============================================================================
# SECURITY - Configuración básica para desarrollo
# =============================================================================

SECRET_KEY = 'django-insecure-dev-local-key-change-in-production'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_CREDENTIALS = True

# =============================================================================
# STATIC FILES - Configuración básica
# =============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# =============================================================================
# EMAIL - Configuración para desarrollo
# =============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

# =============================================================================
# CELERY - Deshabilitado para desarrollo local
# =============================================================================

CELERY_BROKER_URL = None
CELERY_RESULT_BACKEND = None
CELERY_TASK_ALWAYS_EAGER = True  # Ejecutar tareas sincrónicamente

# =============================================================================
# TELEMETRÍA - Configuración desde variables de entorno
# =============================================================================

# Habilitar apps de telemetría desde variables de entorno
TELEMETRY_ENABLED = os.getenv('TELEMETRY_ENABLED', 'True').lower() == 'true'
COMPLIANCE_ENABLED = os.getenv('COMPLIANCE_ENABLED', 'True').lower() == 'true'
CATCHMENT_ENABLED = os.getenv('CATCHMENT_ENABLED', 'True').lower() == 'true'
PROVIDERS_ENABLED = os.getenv('PROVIDERS_ENABLED', 'True').lower() == 'true'
VARIABLES_ENABLED = os.getenv('VARIABLES_ENABLED', 'True').lower() == 'true'

# =============================================================================
# CONFIGURACIONES ESPECÍFICAS PARA TESTING
# =============================================================================

# Configuración para testing de endpoints
TESTING_ENDPOINTS = True

# Configuración de base de datos para testing
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }

# =============================================================================
# CONFIGURACIONES DE DESARROLLO
# =============================================================================

# Mostrar queries SQL en consola
if DEBUG:
    LOGGING['loggers']['django.db.backends'] = {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': False,
    }

# Configuración para desarrollo local
DEVELOPMENT_MODE = True
LOCAL_TESTING = True

# =============================================================================
# CONFIGURACIÓN DRF SPECTACULAR - Documentación automática
# =============================================================================

SPECTACULAR_SETTINGS = {
    'TITLE': 'Stack VPS API - Desarrollo Local',
    'DESCRIPTION': '''
    API de desarrollo local para testing de endpoints.
    
    ## Características:
    - ✅ Solo modelo base (sin telemetría)
    - ✅ SQLite para desarrollo rápido
    - ✅ API de dos capas (base + frontend)
    - ✅ Sistema de caché implementado
    
    ## Endpoints disponibles:
    - **API Base**: `/api/base/` - Servicio interno
    - **API Frontend**: `/api/frontend/` - Capa externa
    - **Admin**: `/admin/` - Panel de administración
    
    ## Autenticación:
    - Usuario: `admin`
    - Contraseña: `admin123`
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/',
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    'REDOC_UI_SETTINGS': {
        'hideDownloadButton': True,
        'hideHostname': True,
    },
    'TAGS': [
        {'name': 'API Base', 'description': 'Endpoints del servicio interno'},
        {'name': 'API Frontend', 'description': 'Endpoints de la capa externa'},
        {'name': 'Variables', 'description': 'Gestión de variables'},
        {'name': 'Esquemas', 'description': 'Gestión de esquemas'},
        {'name': 'Usuarios', 'description': 'Gestión de usuarios'},
        {'name': 'Dashboard', 'description': 'Endpoints para dashboard'},
    ],
}

print("🚀 Configuración de desarrollo local cargada")
print("📊 Base de datos: SQLite")
print("🔧 Apps activas: Core, Users, Providers, Variables, Catchment, Compliance, Telemetry, Frontend")
print("📡 Telemetría: Habilitada")
print("🧪 Modo: Sistema completo")
print("📚 Documentación: /api/schema/swagger-ui/") 