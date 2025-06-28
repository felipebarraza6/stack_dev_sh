from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import asyncio
import logging
from typing import List, Dict, Any
import os
from datetime import datetime
import pytz

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SmartHydro Telemetry Collector",
    description="Servicio para recolección de datos de telemetría desde múltiples proveedores",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración
DJANGO_API_URL = os.getenv("DJANGO_API_URL", "http://business-api:8004")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
KAFKA_BROKERS = os.getenv("KAFKA_BROKERS", "kafka:9092")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Zona horaria de Chile
CHILE_TZ = pytz.timezone('America/Santiago')

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "telemetry-collector",
        "timestamp": datetime.now(CHILE_TZ).isoformat(),
        "version": "1.0.0"
    }

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    try:
        # Verificar conexión con Django
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{DJANGO_API_URL}/health", timeout=5)
            if response.status_code != 200:
                raise HTTPException(status_code=503, detail="Django API not available")
        
        return {"status": "ready"}
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail="Service not ready")

@app.get("/catchment-points/{frequency}")
async def get_catchment_points(frequency: str):
    """Obtener puntos de captación desde Django API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{DJANGO_API_URL}/api/catchment-points/",
                params={"frequency": frequency, "is_telemetry": True},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        logger.error(f"Error connecting to Django API: {e}")
        raise HTTPException(status_code=503, detail="Django API connection failed")
    except httpx.HTTPStatusError as e:
        logger.error(f"Django API error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail="Django API error")

@app.post("/collect/{provider}")
async def collect_data(provider: str, background_tasks: BackgroundTasks):
    """Iniciar recolección de datos para un proveedor específico"""
    try:
        # Obtener puntos de captación desde Django
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{DJANGO_API_URL}/api/catchment-points/",
                params={"provider": provider, "is_telemetry": True},
                timeout=10
            )
            response.raise_for_status()
            points = response.json()
        
        if not points:
            return {"message": f"No points found for provider {provider}"}
        
        # Iniciar recolección en background
        background_tasks.add_task(collect_provider_data, provider, points)
        
        return {
            "message": f"Collection started for {provider}",
            "points_count": len(points),
            "provider": provider
        }
        
    except Exception as e:
        logger.error(f"Error starting collection for {provider}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def collect_provider_data(provider: str, points: List[Dict[str, Any]]):
    """Recolectar datos de un proveedor específico"""
    logger.info(f"Starting data collection for {provider} with {len(points)} points")
    
    for point in points:
        try:
            # Aquí implementaremos la lógica específica de cada proveedor
            await collect_point_data(provider, point)
            
        except Exception as e:
            logger.error(f"Error collecting data for point {point.get('id')}: {e}")
            continue

async def collect_point_data(provider: str, point: Dict[str, Any]):
    """Recolectar datos de un punto específico"""
    point_id = point.get('id')
    logger.info(f"Collecting data for point {point_id} from {provider}")
    
    # TODO: Implementar lógica específica de cada proveedor
    # Por ahora solo log
    logger.info(f"Point {point_id} data collected successfully")

@app.get("/metrics")
async def get_metrics():
    """Obtener métricas del servicio"""
    return {
        "service": "telemetry-collector",
        "timestamp": datetime.now(CHILE_TZ).isoformat(),
        "status": "running",
        "providers": ["twin", "nettra", "novus"],
        "supported_frequencies": ["1", "5", "60"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 