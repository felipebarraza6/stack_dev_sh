"""
Configuración de Tareas para Producción
Configuración más estricta y eficiente para producción
"""
from .base import CELERY_BEAT_SCHEDULE, CELERY_TIMEZONE, CELERY_TASK_ANNOTATIONS
from celery.schedules import crontab

# Configuración para producción - tareas más frecuentes
CELERY_BEAT_SCHEDULE_PROD = CELERY_BEAT_SCHEDULE.copy()

# Modificar frecuencias para producción
CELERY_BEAT_SCHEDULE_PROD.update({
    'sync-telemetry-sources': {
        'task': 'api.tasks.telemetry.sync_telemetry_sources',
        'schedule': crontab(minute='*/2'),  # Cada 2 minutos en producción
    },
    'health-check': {
        'task': 'api.tasks.telemetry.health_check',
        'schedule': crontab(minute='*/5'),  # Cada 5 minutos en producción
    },
    'validate-telemetry-data': {
        'task': 'api.tasks.telemetry.validate_telemetry_data',
        'schedule': crontab(minute='*/10'),  # Cada 10 minutos en producción
    },
    'sync-compliance-sources': {
        'task': 'api.tasks.compliance.sync_compliance_sources',
        'schedule': crontab(hour='*/1'),  # Cada hora en producción
    },
    'validate-compliance-data': {
        'task': 'api.tasks.compliance.validate_compliance_data',
        'schedule': crontab(minute='*/15'),  # Cada 15 minutos en producción
    },
})

# Configuración específica para producción
PROD_CONFIG = {
    'CELERY_TASK_SOFT_TIME_LIMIT': 300,  # 5 minutos en producción
    'CELERY_TASK_TIME_LIMIT': 600,       # 10 minutos en producción
    'CELERY_TASK_ALWAYS_EAGER': False,   # Tareas asíncronas
    'CELERY_TASK_EAGER_PROPAGATES': False,
    'CELERY_WORKER_PREFETCH_MULTIPLIER': 4,
    'CELERY_WORKER_MAX_TASKS_PER_CHILD': 10000,
    'CELERY_WORKER_DISABLE_RATE_LIMITS': False,
    'CELERY_WORKER_CONCURRENCY': 8,
    'CELERY_WORKER_POOL': 'prefork',
    'CELERY_WORKER_AUTOSCALE': '4,8',
} 