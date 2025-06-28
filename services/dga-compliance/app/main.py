"""
Servicio DGA Compliance - FastAPI
Migra la lógica de cronjobs DGA a microservicio optimizado
"""
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, List
import uvicorn

from .dga_processor import DgaProcessor

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="SmartHydro DGA Compliance Service",
    description="Servicio optimizado para cumplimiento DGA",
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

# Instanciar procesador DGA
dga_processor = DgaProcessor()

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "service": "SmartHydro DGA Compliance",
        "version": "2.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check del servicio"""
    return {
        "status": "healthy",
        "service": "dga-compliance",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/process-dga-queue")
async def process_dga_queue(background_tasks: BackgroundTasks, limit: int = 10):
    """
    Procesa cola de datos DGA
    Migra la funcionalidad de cron_dga.py
    """
    try:
        logger.info(f"Iniciando procesamiento de cola DGA con límite: {limit}")
        
        # Ejecutar en background para no bloquear
        background_tasks.add_task(dga_processor.process_dga_queue, limit)
        
        return {
            "message": "Procesamiento DGA iniciado en background",
            "limit": limit,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error iniciando procesamiento DGA: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dga-status")
async def get_dga_status():
    """
    Obtiene estado del servicio DGA
    """
    try:
        # Obtener datos pendientes
        pending_data = await dga_processor.get_pending_dga_data(5)
        
        return {
            "status": "operational",
            "pending_records": len(pending_data),
            "last_check": datetime.now().isoformat(),
            "service_url": dga_processor.dga_url
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo estado DGA: {e}")
        return {
            "status": "error",
            "error": str(e),
            "last_check": datetime.now().isoformat()
        }

@app.post("/send-single-dga")
async def send_single_dga(data: Dict[str, Any]):
    """
    Envía un registro individual a DGA
    Para pruebas y envíos manuales
    """
    try:
        from .dga_processor import DgaData
        
        # Convertir datos a modelo DgaData
        dga_data = DgaData(
            catchment_point_id=data.get('catchment_point_id'),
            catchment_point_title=data.get('catchment_point_title', 'Test'),
            date_time_medition=datetime.fromisoformat(data.get('date_time_medition')),
            total=data.get('total'),
            flow=data.get('flow'),
            water_table=data.get('water_table'),
            code_dga=data.get('code_dga', 'TEST001'),
            type_dga=data.get('type_dga', 'SUBTERRANEO'),
            rut=data.get('rut', '12345678-9'),
            password=data.get('password', 'test'),
            interaction_id=data.get('interaction_id', 999)
        )
        
        result = await dga_processor.send_to_dga(dga_data)
        
        return {
            "message": "Envío DGA completado",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error en envío individual DGA: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dga-config")
async def get_dga_config():
    """
    Obtiene configuración del servicio DGA
    """
    return {
        "service_url": dga_processor.dga_url,
        "headers": dga_processor.headers,
        "timeout": 30,
        "max_retries": 3,
        "retry_delay": 10,
        "success_delay": 20
    }

# Tarea programada (reemplaza cronjob)
@app.on_event("startup")
async def startup_event():
    """Evento de inicio del servicio"""
    logger.info("🚀 Servicio DGA Compliance iniciado")
    logger.info("📊 Migrado desde cronjobs Django a FastAPI")
    logger.info("⚡ Optimizado para alta concurrencia")

@app.on_event("shutdown")
async def shutdown_event():
    """Evento de cierre del servicio"""
    logger.info("🛑 Servicio DGA Compliance detenido")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    ) 