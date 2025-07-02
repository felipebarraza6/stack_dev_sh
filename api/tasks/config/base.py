"""
Configuración Base de Tareas Programadas
Configuración común para todos los entornos
"""
from celery.schedules import crontab

# Configuración base de tareas programadas
CELERY_BEAT_SCHEDULE = {
    # Tareas de Telemetría
    'sync-telemetry-sources': {
        'task': 'api.tasks.telemetry.sync_telemetry_sources',
        'schedule': crontab(minute='*/5'),  # Cada 5 minutos
    },
    'validate-telemetry-data': {
        'task': 'api.tasks.telemetry.validate_telemetry_data',
        'schedule': crontab(minute='*/15'),  # Cada 15 minutos
    },
    'health-check': {
        'task': 'api.tasks.telemetry.health_check',
        'schedule': crontab(minute='*/10'),  # Cada 10 minutos
    },
    'cleanup-old-data': {
        'task': 'api.tasks.telemetry.cleanup_old_data',
        'schedule': crontab(hour=2, minute=0),  # Diario a las 2:00 AM
    },
    'generate-telemetry-report': {
        'task': 'api.tasks.telemetry.generate_telemetry_report',
        'schedule': crontab(hour=6, minute=0),  # Diario a las 6:00 AM
    },
    
    # Tareas de Cumplimiento
    'daily-compliance-report': {
        'task': 'api.tasks.compliance.daily_compliance_report',
        'schedule': crontab(hour=7, minute=0),  # Diario a las 7:00 AM
    },
    'sync-compliance-sources': {
        'task': 'api.tasks.compliance.sync_compliance_sources',
        'schedule': crontab(hour='*/2'),  # Cada 2 horas
    },
    'validate-compliance-data': {
        'task': 'api.tasks.compliance.validate_compliance_data',
        'schedule': crontab(minute='*/30'),  # Cada 30 minutos
    },
    'cleanup-compliance-logs': {
        'task': 'api.tasks.compliance.cleanup_compliance_logs',
        'schedule': crontab(hour=3, minute=0),  # Diario a las 3:00 AM
    },
    
    # Tareas de Notificaciones
    'send-daily-summary': {
        'task': 'api.tasks.notifications.send_daily_summary',
        'schedule': crontab(hour=8, minute=0),  # Diario a las 8:00 AM
    },
}

# Configuración de timezone
CELERY_TIMEZONE = 'America/Santiago'

# Configuración de expiración de tareas
CELERY_TASK_SOFT_TIME_LIMIT = 300  # 5 minutos
CELERY_TASK_TIME_LIMIT = 600       # 10 minutos

# Configuración de reintentos
CELERY_TASK_ANNOTATIONS = {
    '*': {
        'retry_backoff': True,
        'retry_backoff_max': 600,
        'max_retries': 3,
    }
} 