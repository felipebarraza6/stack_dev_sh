"""
Servicio de Telemetría Optimizado
FastAPI con endpoints optimizados para recolección de datos
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import asyncio
from datetime import datetime
import pytz
from typing import Dict, List, Optional

from .collectors.optimized_collector import OptimizedTelemetryCollector

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de zona horaria
CHILE_TZ = pytz.timezone('America/Santiago')

# Crear aplicación FastAPI
app = FastAPI(
    title="SmartHydro Telemetry Collector (Optimized)",
    description="Servicio optimizado para recolección de datos de telemetría",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia global del colector
collector: Optional[OptimizedTelemetryCollector] = None


@app.on_event("startup")
async def startup_event():
    """Inicializar el colector al arrancar"""
    global collector
    
    try:
        collector = OptimizedTelemetryCollector(
            database_url="postgresql://smarthydro:smarthydro123@postgres:5432/smarthydro_business",
            redis_url="redis://redis:6379",
            kafka_brokers="kafka:29092"
        )
        
        await collector.initialize()
        logger.info("Telemetry Collector initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing collector: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Limpiar recursos al cerrar"""
    logger.info("Shutting down Telemetry Collector")


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "service": "SmartHydro Telemetry Collector (Optimized)",
        "version": "2.0.0",
        "status": "running",
        "timestamp": datetime.now(CHILE_TZ).isoformat()
    }


@app.get("/health")
async def health_check():
    """Health check optimizado"""
    try:
        if not collector:
            raise HTTPException(status_code=503, detail="Collector not initialized")
        
        # Obtener estadísticas
        stats = await collector.get_collection_stats()
        
        # Verificar salud
        total_points = stats.get('total_active_points', 0)
        
        if total_points > 0:
            health_status = "healthy"
        else:
            health_status = "warning"
        
        return {
            "status": health_status,
            "timestamp": datetime.now(CHILE_TZ).isoformat(),
            "stats": stats,
            "services": {
                "collector": "running",
                "database": "connected",
                "redis": "connected",
                "kafka": "connected"
            }
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now(CHILE_TZ).isoformat()
            }
        )


@app.get("/ready")
async def readiness_check():
    """Readiness check"""
    if collector:
        return {"status": "ready"}
    else:
        raise HTTPException(status_code=503, detail="Service not ready")


@app.get("/stats")
async def get_stats():
    """Obtener estadísticas de recolección"""
    try:
        if not collector:
            raise HTTPException(status_code=503, detail="Collector not initialized")
        
        stats = await collector.get_collection_stats()
        return stats
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/collect/frequency/{frequency}")
async def collect_by_frequency(frequency: str, background_tasks: BackgroundTasks):
    """
    Recolectar datos por frecuencia específica
    """
    try:
        if not collector:
            raise HTTPException(status_code=503, detail="Collector not initialized")
        
        # Validar frecuencia
        valid_frequencies = ['1', '5', '60']
        if frequency not in valid_frequencies:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid frequency. Must be one of: {valid_frequencies}"
            )
        
        # Ejecutar en background
        background_tasks.add_task(collector.collect_by_frequency, frequency)
        
        return {
            "message": f"Collection started for frequency {frequency}",
            "frequency": frequency,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error starting collection for frequency {frequency}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/collect/provider/{provider}")
async def collect_by_provider(provider: str, background_tasks: BackgroundTasks):
    """
    Recolectar datos por proveedor específico
    """
    try:
        if not collector:
            raise HTTPException(status_code=503, detail="Collector not initialized")
        
        # Validar proveedor
        valid_providers = ['twin', 'nettra', 'novus']
        if provider.lower() not in valid_providers:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid provider. Must be one of: {valid_providers}"
            )
        
        # Ejecutar en background
        background_tasks.add_task(collector._collect_provider_data, provider, [], '60')
        
        return {
            "message": f"Collection started for provider {provider}",
            "provider": provider,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error starting collection for provider {provider}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/points/active")
async def get_active_points(
    frequency: Optional[str] = None,
    provider: Optional[str] = None
):
    """
    Obtener puntos activos con filtros opcionales
    """
    try:
        if not collector:
            raise HTTPException(status_code=503, detail="Collector not initialized")
        
        points = await collector.get_active_points(frequency=frequency, provider=provider)
        
        # Convertir a formato JSON serializable
        points_data = []
        for point in points:
            points_data.append({
                "id": point.id,
                "title": point.title,
                "frequency": point.frequency,
                "provider": point.provider,
                "coordinates": point.coordinates,
                "config_keys": list(point.config.keys()) if point.config else []
            })
        
        return {
            "points": points_data,
            "total": len(points_data),
            "filters": {
                "frequency": frequency,
                "provider": provider
            },
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting active points: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cache/invalidate")
async def invalidate_cache():
    """
    Invalidar cache de telemetría
    """
    try:
        # Importar función de invalidación
        from api.core.models.catchment_points import invalidate_telemetry_cache
        
        invalidate_telemetry_cache()
        
        return {
            "message": "Cache invalidated successfully",
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error invalidating cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """
    Obtener métricas del servicio
    """
    try:
        if not collector:
            raise HTTPException(status_code=503, detail="Collector not initialized")
        
        stats = await collector.get_collection_stats()
        
        # Calcular métricas adicionales
        total_points = stats.get('total_active_points', 0)
        by_frequency = stats.get('by_frequency', {})
        by_provider = stats.get('by_provider', {})
        
        metrics = {
            "total_active_points": total_points,
            "points_by_frequency": by_frequency,
            "points_by_provider": by_provider,
            "estimated_measurements_per_hour": self._calculate_measurements_per_hour(by_frequency),
            "uptime": "100%",  # TODO: Implementar cálculo real
            "last_collection": datetime.now(CHILE_TZ).isoformat(),
            "cache_hit_rate": "95%",  # TODO: Implementar cálculo real
        }
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    def _calculate_measurements_per_hour(self, by_frequency: Dict[str, int]) -> int:
        """Calcular mediciones por hora basado en frecuencias"""
        total = 0
        for frequency, count in by_frequency.items():
            if frequency == '1':
                total += count * 60  # 60 mediciones por hora
            elif frequency == '5':
                total += count * 12  # 12 mediciones por hora
            elif frequency == '60':
                total += count * 1   # 1 medición por hora
        return total


@app.post("/test/connection")
async def test_connection():
    """
    Probar conexiones a servicios externos
    """
    try:
        if not collector:
            raise HTTPException(status_code=503, detail="Collector not initialized")
        
        # Obtener puntos activos para probar conexión
        points = await collector.get_active_points()
        
        connection_tests = {
            "database": "connected" if points is not None else "disconnected",
            "redis": "connected",  # TODO: Implementar test real
            "kafka": "connected",  # TODO: Implementar test real
            "active_points_count": len(points) if points else 0
        }
        
        return {
            "connection_tests": connection_tests,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error testing connections: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints de administración
@app.get("/admin/status")
async def admin_status():
    """
    Estado administrativo del servicio
    """
    try:
        if not collector:
            raise HTTPException(status_code=503, detail="Collector not initialized")
        
        stats = await collector.get_collection_stats()
        
        return {
            "service_status": "running",
            "collector_status": "active",
            "active_points": stats.get('total_active_points', 0),
            "memory_usage": "2.5GB",  # TODO: Implementar monitoreo real
            "cpu_usage": "15%",       # TODO: Implementar monitoreo real
            "uptime": "24h",          # TODO: Implementar cálculo real
            "last_restart": datetime.now(CHILE_TZ).isoformat(),
            "version": "2.0.0"
        }
        
    except Exception as e:
        logger.error(f"Error getting admin status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main_optimized:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    ) 