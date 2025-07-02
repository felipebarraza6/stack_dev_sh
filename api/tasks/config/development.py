"""
Configuración de Tareas para Desarrollo
Configuración más permisiva para facilitar el desarrollo
"""
from .base import CELERY_BEAT_SCHEDULE, CELERY_TIMEZONE, CELERY_TASK_ANNOTATIONS
from celery.schedules import crontab

# Configuración para desarrollo - tareas menos frecuentes
CELERY_BEAT_SCHEDULE_DEV = CELERY_BEAT_SCHEDULE.copy()

# Modificar frecuencias para desarrollo
CELERY_BEAT_SCHEDULE_DEV.update({
    'sync-telemetry-sources': {
        'task': 'api.tasks.telemetry.sync_telemetry_sources',
        'schedule': crontab(minute='*/15'),  # Cada 15 minutos en desarrollo
    },
    'health-check': {
        'task': 'api.tasks.telemetry.health_check',
        'schedule': crontab(minute='*/30'),  # Cada 30 minutos en desarrollo
    },
    'validate-telemetry-data': {
        'task': 'api.tasks.telemetry.validate_telemetry_data',
        'schedule': crontab(minute='*/45'),  # Cada 45 minutos en desarrollo
    },
    'sync-compliance-sources': {
        'task': 'api.tasks.compliance.sync_compliance_sources',
        'schedule': crontab(hour='*/4'),  # Cada 4 horas en desarrollo
    },
    'validate-compliance-data': {
        'task': 'api.tasks.compliance.validate_compliance_data',
        'schedule': crontab(hour='*/1'),  # Cada hora en desarrollo
    },
})

# Configuración específica para desarrollo
DEV_CONFIG = {
    'CELERY_TASK_SOFT_TIME_LIMIT': 600,  # 10 minutos en desarrollo
    'CELERY_TASK_TIME_LIMIT': 1200,      # 20 minutos en desarrollo
    'CELERY_TASK_ALWAYS_EAGER': False,   # Tareas asíncronas
    'CELERY_TASK_EAGER_PROPAGATES': True,
    'CELERY_WORKER_PREFETCH_MULTIPLIER': 1,
    'CELERY_WORKER_MAX_TASKS_PER_CHILD': 1000,
    'CELERY_WORKER_DISABLE_RATE_LIMITS': True,
} 