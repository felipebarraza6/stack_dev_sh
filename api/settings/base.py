"""
Configuración base para el proyecto SmartHydro
Configuraciones comunes para todos los entornos
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'h#v#*68y)bfb2ylvy^f-tksars9-k1#8lejxo==_3hsnu2ek!h')

# Application definition
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',
    'django_rest_passwordreset',
    'channels',  # Django Channels para WebSockets
]

LOCAL_APPS = [
    # App base con modelos y utilidades compartidas
    'api.apps.common.apps.CommonConfig',

    # Aplicaciones principales del proyecto
    'api.apps.telemetry.apps.TelemetryConfig',
    'api.apps.users.apps.UsersConfig',
    'api.apps.erp.apps.ErpConfig',
    'api.apps.support.apps.SupportConfig',
    'api.apps.datastore.apps.DatastoreConfig',
    'api.apps.notifications.apps.NotificationsConfig',
    
    # Herramientas de terceros para apps locales
    'import_export'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'api.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Custom user model
AUTH_USER_MODEL = 'users.User'

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'drf_excel.renderers.XLSXRenderer'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend'
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# CORS configuration
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:3001',
]

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'mail.smarthydro.cl')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 465))
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'felipebarraza@smarthydro.cl')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'vhhwk2013go')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'felipebarraza@smarthydro.cl')

# Configuración de microservicios (telemetría y DGA migrados a FastAPI)
MICROSERVICES = {
    'telemetry_collector': os.environ.get('TELEMETRY_SERVICE_URL', 'http://telemetry-collector:8001'),
    'dga_compliance': os.environ.get('DGA_SERVICE_URL', 'http://dga-compliance:8002'),
    'business_api': os.environ.get('BUSINESS_API_URL', 'http://business-api:8004')
}

# =============================================================================
# DJANGO CHANNELS CONFIGURATION
# =============================================================================

# Configuración de Channels para WebSockets
ASGI_APPLICATION = 'api.asgi.application'

# Configuración del backend de channels (Redis)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [
                {
                    'host': os.environ.get('REDIS_HOST', 'redis'),
                    'port': int(os.environ.get('REDIS_PORT', 6379)),
                    'password': os.environ.get('REDIS_PASSWORD', 'smarthydro123'),
                }
            ],
        },
    },
}

# Configuración de Redis para cache y sessions
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://:{os.environ.get('REDIS_PASSWORD', 'smarthydro123')}@{os.environ.get('REDIS_HOST', 'redis')}:{os.environ.get('REDIS_PORT', 6379)}/1",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Configuración de sesiones con Redis
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# =============================================================================
# NOTIFICATIONS CONFIGURATION
# =============================================================================

# Configuración de notificaciones
NOTIFICATION_SETTINGS = {
    'ENABLE_REALTIME': True,
    'ENABLE_EMAIL': True,
    'ENABLE_PUSH': False,  # Para futuras implementaciones
    'DEFAULT_CHANNEL': 'general',
    'USER_CHANNEL_PREFIX': 'user_',
    'PROJECT_CHANNEL_PREFIX': 'project_',
    'TICKET_CHANNEL_PREFIX': 'ticket_',
}

# Tipos de notificaciones disponibles
NOTIFICATION_TYPES = {
    'TASK_ASSIGNED': 'task_assigned',
    'TASK_STATUS_CHANGED': 'task_status_changed',
    'TICKET_CREATED': 'ticket_created',
    'TICKET_UPDATED': 'ticket_updated',
    'TICKET_ASSIGNED': 'ticket_assigned',
    'QUOTATION_APPROVED': 'quotation_approved',
    'QUOTATION_REJECTED': 'quotation_rejected',
    'PAYMENT_RECEIVED': 'payment_received',
    'SYSTEM_ALERT': 'system_alert',
    'TELEMETRY_ALERT': 'telemetry_alert',
} 