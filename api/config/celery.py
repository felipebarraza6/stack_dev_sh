"""
Configuración de Celery
Sistema profesional de tareas en background
"""
import os
from celery import Celery
from django.conf import settings

# Configurar el módulo de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.config.settings.development')

# Crear la aplicación Celery
app = Celery('stack_vps')

# Configurar Celery usando la configuración de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Cargar tareas automáticamente desde todas las apps registradas
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Configuración de Celery
app.conf.update(
    # Broker de mensajes
    broker_url=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    result_backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    
    # Configuración de tareas
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Santiago',
    enable_utc=True,
    
    # Configuración de workers
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    
    # Configuración de beat (tareas programadas)
    beat_schedule={
        # Tareas diarias
        'daily-compliance-report': {
            'task': 'tasks.telemetry.daily_compliance_report',
            'schedule': 86400.0,  # 24 horas
        },
        'cleanup-old-data': {
            'task': 'tasks.telemetry.cleanup_old_data',
            'schedule': 86400.0,  # 24 horas
        },
        'health-check': {
            'task': 'tasks.telemetry.health_check',
            'schedule': 3600.0,  # 1 hora
        },
        
        # Tareas de cumplimiento (cada 6 horas)
        'sync-compliance-sources': {
            'task': 'tasks.telemetry.sync_compliance_sources',
            'schedule': 21600.0,  # 6 horas
        },
        
        # Tareas de telemetría (cada 5 minutos)
        'process-telemetry-batch': {
            'task': 'tasks.telemetry.process_telemetry_batch',
            'schedule': 300.0,  # 5 minutos
        },
    },
    
    # Configuración de retry
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    
    # Configuración de logs
    worker_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    worker_task_log_format='[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s%(task_id)s)] %(message)s',
)


@app.task(bind=True)
def debug_task(self):
    """Tarea de debug para testing"""
    print(f'Request: {self.request!r}')
    return 'Debug task completed'


# Configuración de rutas de tareas
app.conf.task_routes = {
    'tasks.telemetry.*': {'queue': 'telemetry'},
    'tasks.compliance.*': {'queue': 'compliance'},
    'tasks.notifications.*': {'queue': 'notifications'},
    'tasks.reports.*': {'queue': 'reports'},
}