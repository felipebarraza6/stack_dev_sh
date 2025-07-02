"""
Configuración de desarrollo
"""
from .base import *
import os

# Configuración específica para desarrollo
DEBUG = True

# Configuración de DRF para desarrollo
from api.config.drf.development import REST_FRAMEWORK_DEV
REST_FRAMEWORK = REST_FRAMEWORK_DEV

# Configuración de tareas para desarrollo
from api.tasks.config.development import CELERY_BEAT_SCHEDULE_DEV, DEV_CONFIG
CELERY_BEAT_SCHEDULE = CELERY_BEAT_SCHEDULE_DEV

# Aplicar configuración específica de desarrollo
CELERY_TASK_SOFT_TIME_LIMIT = DEV_CONFIG['CELERY_TASK_SOFT_TIME_LIMIT']
CELERY_TASK_TIME_LIMIT = DEV_CONFIG['CELERY_TASK_TIME_LIMIT']
CELERY_TASK_ALWAYS_EAGER = DEV_CONFIG['CELERY_TASK_ALWAYS_EAGER']
CELERY_TASK_EAGER_PROPAGATES = DEV_CONFIG['CELERY_TASK_EAGER_PROPAGATES']
CELERY_WORKER_PREFETCH_MULTIPLIER = DEV_CONFIG['CELERY_WORKER_PREFETCH_MULTIPLIER']
CELERY_WORKER_MAX_TASKS_PER_CHILD = DEV_CONFIG['CELERY_WORKER_MAX_TASKS_PER_CHILD']
CELERY_WORKER_DISABLE_RATE_LIMITS = DEV_CONFIG['CELERY_WORKER_DISABLE_RATE_LIMITS']

# Configuración de base de datos para desarrollo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Configuración de CORS más permisiva para desarrollo
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:3001',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8000',
]

# Configuración de logging para desarrollo
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/development.log',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'rest_framework': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
} 