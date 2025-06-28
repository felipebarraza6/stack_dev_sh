"""
Celery application for Telemetry Collector
Programa las tareas de recolección de datos
"""
from celery import Celery
from celery.schedules import crontab
import os

# Configuración
DJANGO_API_URL = os.getenv("DJANGO_API_URL", "http://business-api:8004")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
KAFKA_BROKERS = os.getenv("KAFKA_BROKERS", "kafka:9092")

# Crear aplicación Celery
app = Celery(
    'telemetry_collector',
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['app.tasks']
)

# Configuración de Celery
app.conf.update(
    # Configuración de tareas
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Santiago',
    enable_utc=True,
    
    # Configuración de workers
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_max_tasks_per_child=1000,
    
    # Configuración de beat (scheduler)
    beat_schedule={
        # Twin (TData) - Cada minuto
        'collect-twin-1min': {
            'task': 'app.tasks.collect_twin_data',
            'schedule': crontab(minute='*'),
            'args': ('1',),
            'options': {'queue': 'telemetry'}
        },
        
        # Twin (TData) - Cada 5 minutos
        'collect-twin-5min': {
            'task': 'app.tasks.collect_twin_data',
            'schedule': crontab(minute='*/5'),
            'args': ('5',),
            'options': {'queue': 'telemetry'}
        },
        
        # Twin (TData) - Cada hora
        'collect-twin-1hour': {
            'task': 'app.tasks.collect_twin_data',
            'schedule': crontab(minute=0, hour='*'),
            'args': ('60',),
            'options': {'queue': 'telemetry'}
        },
        
        # Nettra - Cada 5 minutos
        'collect-nettra-5min': {
            'task': 'app.tasks.collect_nettra_data',
            'schedule': crontab(minute='*/5'),
            'args': ('5',),
            'options': {'queue': 'telemetry'}
        },
        
        # Nettra - Cada hora
        'collect-nettra-1hour': {
            'task': 'app.tasks.collect_nettra_data',
            'schedule': crontab(minute=0, hour='*'),
            'args': ('60',),
            'options': {'queue': 'telemetry'}
        },
        
        # Novus - Cada hora
        'collect-novus-1hour': {
            'task': 'app.tasks.collect_novus_data',
            'schedule': crontab(minute=0, hour='*'),
            'args': ('60',),
            'options': {'queue': 'telemetry'}
        },
    },
    
    # Configuración de colas
    task_routes={
        'app.tasks.*': {'queue': 'telemetry'},
    },
    
    # Configuración de resultados
    result_expires=3600,  # 1 hora
    
    # Configuración de logs
    worker_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    worker_task_log_format='[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s',
)

if __name__ == '__main__':
    app.start() 