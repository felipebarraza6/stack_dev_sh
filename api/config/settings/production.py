"""
Configuración de producción
"""
from .base import *
import os

# Configuración específica para producción
DEBUG = False

# Configuración de DRF para producción
from api.config.drf.production import REST_FRAMEWORK_PROD
REST_FRAMEWORK = REST_FRAMEWORK_PROD

# Configuración de tareas para producción
from api.tasks.config.production import CELERY_BEAT_SCHEDULE_PROD, PROD_CONFIG
CELERY_BEAT_SCHEDULE = CELERY_BEAT_SCHEDULE_PROD

# Aplicar configuración específica de producción
CELERY_TASK_SOFT_TIME_LIMIT = PROD_CONFIG['CELERY_TASK_SOFT_TIME_LIMIT']
CELERY_TASK_TIME_LIMIT = PROD_CONFIG['CELERY_TASK_TIME_LIMIT']
CELERY_TASK_ALWAYS_EAGER = PROD_CONFIG['CELERY_TASK_ALWAYS_EAGER']
CELERY_TASK_EAGER_PROPAGATES = PROD_CONFIG['CELERY_TASK_EAGER_PROPAGATES']
CELERY_WORKER_PREFETCH_MULTIPLIER = PROD_CONFIG['CELERY_WORKER_PREFETCH_MULTIPLIER']
CELERY_WORKER_MAX_TASKS_PER_CHILD = PROD_CONFIG['CELERY_WORKER_MAX_TASKS_PER_CHILD']
CELERY_WORKER_DISABLE_RATE_LIMITS = PROD_CONFIG['CELERY_WORKER_DISABLE_RATE_LIMITS']
CELERY_WORKER_CONCURRENCY = PROD_CONFIG['CELERY_WORKER_CONCURRENCY']
CELERY_WORKER_POOL = PROD_CONFIG['CELERY_WORKER_POOL']
CELERY_WORKER_AUTOSCALE = PROD_CONFIG['CELERY_WORKER_AUTOSCALE']

# Configuración de seguridad para producción
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Configuración de hosts permitidos en producción
ALLOWED_HOSTS = [
    'smarthydro.app',
    'www.smarthydro.app',
    'api.smarthydro.app',
]

# Configuración de CORS más restrictiva para producción
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    'https://smarthydro.app',
    'https://www.smarthydro.app',
    'https://api.smarthydro.app',
]

# Configuración de base de datos para producción
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'postgres'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Configuración de logging para producción
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logs/production.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'rest_framework': {
            'handlers': ['file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
} 