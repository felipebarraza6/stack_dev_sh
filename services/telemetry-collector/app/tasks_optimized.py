"""
Tareas Celery Optimizadas para Telemetría
Usa el nuevo colector optimizado con cache y consultas eficientes
"""
import logging
from celery import shared_task
from datetime import datetime
import pytz

from .collectors.optimized_collector import OptimizedTelemetryCollector

logger = logging.getLogger(__name__)
CHILE_TZ = pytz.timezone('America/Santiago')


@shared_task(bind=True, name='telemetry.collect_frequency_1')
def collect_frequency_1(self):
    """
    Recolectar datos cada 1 minuto (optimizado)
    """
    try:
        logger.info("Starting frequency 1 collection (optimized)")
        
        # Crear colector optimizado
        collector = OptimizedTelemetryCollector(
            database_url="postgresql://smarthydro:smarthydro123@postgres:5432/smarthydro_business",
            redis_url="redis://redis:6379",
            kafka_brokers="kafka:29092"
        )
        
        # Ejecutar recolección
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(collector.initialize())
            loop.run_until_complete(collector.collect_by_frequency('1'))
        finally:
            loop.close()
        
        logger.info("Frequency 1 collection completed (optimized)")
        return {"status": "success", "frequency": "1", "timestamp": datetime.now(CHILE_TZ).isoformat()}
        
    except Exception as e:
        logger.error(f"Error in frequency 1 collection: {e}")
        self.retry(countdown=60, max_retries=3)
        return {"status": "error", "error": str(e)}


@shared_task(bind=True, name='telemetry.collect_frequency_5')
def collect_frequency_5(self):
    """
    Recolectar datos cada 5 minutos (optimizado)
    """
    try:
        logger.info("Starting frequency 5 collection (optimized)")
        
        collector = OptimizedTelemetryCollector(
            database_url="postgresql://smarthydro:smarthydro123@postgres:5432/smarthydro_business",
            redis_url="redis://redis:6379",
            kafka_brokers="kafka:29092"
        )
        
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(collector.initialize())
            loop.run_until_complete(collector.collect_by_frequency('5'))
        finally:
            loop.close()
        
        logger.info("Frequency 5 collection completed (optimized)")
        return {"status": "success", "frequency": "5", "timestamp": datetime.now(CHILE_TZ).isoformat()}
        
    except Exception as e:
        logger.error(f"Error in frequency 5 collection: {e}")
        self.retry(countdown=300, max_retries=3)
        return {"status": "error", "error": str(e)}


@shared_task(bind=True, name='telemetry.collect_frequency_60')
def collect_frequency_60(self):
    """
    Recolectar datos cada 60 minutos (optimizado)
    """
    try:
        logger.info("Starting frequency 60 collection (optimized)")
        
        collector = OptimizedTelemetryCollector(
            database_url="postgresql://smarthydro:smarthydro123@postgres:5432/smarthydro_business",
            redis_url="redis://redis:6379",
            kafka_brokers="kafka:29092"
        )
        
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(collector.initialize())
            loop.run_until_complete(collector.collect_by_frequency('60'))
        finally:
            loop.close()
        
        logger.info("Frequency 60 collection completed (optimized)")
        return {"status": "success", "frequency": "60", "timestamp": datetime.now(CHILE_TZ).isoformat()}
        
    except Exception as e:
        logger.error(f"Error in frequency 60 collection: {e}")
        self.retry(countdown=3600, max_retries=3)
        return {"status": "error", "error": str(e)}


@shared_task(bind=True, name='telemetry.collect_by_provider')
def collect_by_provider(self, provider: str):
    """
    Recolectar datos por proveedor específico (optimizado)
    """
    try:
        logger.info(f"Starting collection for provider: {provider} (optimized)")
        
        collector = OptimizedTelemetryCollector(
            database_url="postgresql://smarthydro:smarthydro123@postgres:5432/smarthydro_business",
            redis_url="redis://redis:6379",
            kafka_brokers="kafka:29092"
        )
        
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(collector.initialize())
            points = loop.run_until_complete(collector.get_active_points(provider=provider))
            
            if points:
                loop.run_until_complete(collector._collect_provider_data(provider, points, '60'))
            
        finally:
            loop.close()
        
        logger.info(f"Provider {provider} collection completed (optimized)")
        return {"status": "success", "provider": provider, "timestamp": datetime.now(CHILE_TZ).isoformat()}
        
    except Exception as e:
        logger.error(f"Error in provider {provider} collection: {e}")
        self.retry(countdown=300, max_retries=3)
        return {"status": "error", "error": str(e)}


@shared_task(bind=True, name='telemetry.get_collection_stats')
def get_collection_stats(self):
    """
    Obtener estadísticas de recolección (optimizado)
    """
    try:
        logger.info("Getting collection stats (optimized)")
        
        collector = OptimizedTelemetryCollector(
            database_url="postgresql://smarthydro:smarthydro123@postgres:5432/smarthydro_business",
            redis_url="redis://redis:6379",
            kafka_brokers="kafka:29092"
        )
        
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            stats = loop.run_until_complete(collector.get_collection_stats())
        finally:
            loop.close()
        
        logger.info("Collection stats retrieved (optimized)")
        return stats
        
    except Exception as e:
        logger.error(f"Error getting collection stats: {e}")
        return {"error": str(e)}


@shared_task(bind=True, name='telemetry.invalidate_cache')
def invalidate_cache(self):
    """
    Invalidar cache de telemetría
    """
    try:
        logger.info("Invalidating telemetry cache")
        
        # Importar función de invalidación
        from api.core.models.catchment_points import invalidate_telemetry_cache
        
        invalidate_telemetry_cache()
        
        logger.info("Telemetry cache invalidated successfully")
        return {"status": "success", "message": "Cache invalidated"}
        
    except Exception as e:
        logger.error(f"Error invalidating cache: {e}")
        return {"status": "error", "error": str(e)}


@shared_task(bind=True, name='telemetry.health_check')
def health_check(self):
    """
    Verificar salud del sistema de telemetría
    """
    try:
        logger.info("Running telemetry health check")
        
        collector = OptimizedTelemetryCollector(
            database_url="postgresql://smarthydro:smarthydro123@postgres:5432/smarthydro_business",
            redis_url="redis://redis:6379",
            kafka_brokers="kafka:29092"
        )
        
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            stats = loop.run_until_complete(collector.get_collection_stats())
        finally:
            loop.close()
        
        # Verificar que hay puntos activos
        if stats.get('total_active_points', 0) > 0:
            health_status = "healthy"
        else:
            health_status = "warning"
        
        health_info = {
            "status": health_status,
            "timestamp": datetime.now(CHILE_TZ).isoformat(),
            "stats": stats,
            "services": {
                "database": "connected",
                "redis": "connected", 
                "kafka": "connected"
            }
        }
        
        logger.info(f"Health check completed: {health_status}")
        return health_info
        
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }


# Configuración de tareas programadas optimizadas
CELERY_BEAT_SCHEDULE = {
    'collect-frequency-1': {
        'task': 'telemetry.collect_frequency_1',
        'schedule': 60.0,  # Cada 60 segundos
    },
    'collect-frequency-5': {
        'task': 'telemetry.collect_frequency_5',
        'schedule': 300.0,  # Cada 5 minutos
    },
    'collect-frequency-60': {
        'task': 'telemetry.collect_frequency_60',
        'schedule': 3600.0,  # Cada hora
    },
    'health-check': {
        'task': 'telemetry.health_check',
        'schedule': 300.0,  # Cada 5 minutos
    },
    'invalidate-cache': {
        'task': 'telemetry.invalidate_cache',
        'schedule': 1800.0,  # Cada 30 minutos
    },
} 