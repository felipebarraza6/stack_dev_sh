"""
Microservicio de Procesamiento de Datos
Consume datos de Kafka y los almacena en el modelo unificado
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import logging
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import pytz
import httpx
import asyncpg
from aiokafka import AIOKafkaConsumer
from pydantic import BaseModel

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de zona horaria
CHILE_TZ = pytz.timezone('America/Santiago')

# Crear aplicación FastAPI
app = FastAPI(
    title="SmartHydro Data Processor",
    description="Microservicio para procesamiento y almacenamiento de datos de telemetría",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración global
DATABASE_URL = "postgresql://smarthydro:smarthydro123@postgres:5432/smarthydro_business"
KAFKA_BROKERS = "kafka:29092"
DJANGO_API_URL = "http://django:8000"

# Conexiones globales
db_pool: Optional[asyncpg.Pool] = None
kafka_consumer: Optional[AIOKafkaConsumer] = None
http_client: Optional[httpx.AsyncClient] = None


class MeasurementData(BaseModel):
    """Datos de medición recibidos de Kafka"""
    point_id: int
    variable_name: str
    timestamp: datetime
    value: Any
    raw_value: Dict[str, Any]
    provider: str
    quality_score: float = 1.0
    processing_config: Dict[str, Any] = {}
    days_since_last_connection: int = 0


class BatchData(BaseModel):
    """Datos de lote para procesamiento"""
    batch_id: str
    provider: str
    frequency: str
    measurements: List[MeasurementData]
    metadata: Dict[str, Any] = {}


@app.on_event("startup")
async def startup_event():
    """Inicializar conexiones al arrancar"""
    global db_pool, kafka_consumer, http_client
    
    try:
        # Conectar a PostgreSQL
        db_pool = await asyncpg.create_pool(DATABASE_URL)
        logger.info("Connected to PostgreSQL")
        
        # Conectar a Kafka
        kafka_consumer = AIOKafkaConsumer(
            'measurements',
            bootstrap_servers=KAFKA_BROKERS,
            group_id='data-processor-group',
            auto_offset_reset='latest',
            enable_auto_commit=True,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        await kafka_consumer.start()
        logger.info("Connected to Kafka")
        
        # Crear cliente HTTP
        http_client = httpx.AsyncClient(timeout=30.0)
        logger.info("HTTP client created")
        
        # Iniciar procesamiento en background
        asyncio.create_task(process_kafka_messages())
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Limpiar conexiones al cerrar"""
    global db_pool, kafka_consumer, http_client
    
    if kafka_consumer:
        await kafka_consumer.stop()
        logger.info("Kafka consumer stopped")
    
    if db_pool:
        await db_pool.close()
        logger.info("Database connection closed")
    
    if http_client:
        await http_client.aclose()
        logger.info("HTTP client closed")


async def process_kafka_messages():
    """Procesar mensajes de Kafka en loop continuo"""
    global kafka_consumer
    
    try:
        async for message in kafka_consumer:
            try:
                # Procesar mensaje
                await process_measurement_message(message.value)
                
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                continue
                
    except Exception as e:
        logger.error(f"Error in Kafka processing loop: {e}")


async def process_measurement_message(data: Dict[str, Any]):
    """Procesar un mensaje de medición individual"""
    try:
        # Validar datos
        measurement_data = MeasurementData(**data)
        
        # Obtener variable desde Django API
        variable = await get_variable_by_name(measurement_data.variable_name)
        if not variable:
            logger.warning(f"Variable not found: {measurement_data.variable_name}")
            return
        
        # Crear medición en base de datos
        await create_measurement(measurement_data, variable['id'])
        
        logger.info(f"Processed measurement: {measurement_data.point_id} - {measurement_data.variable_name}")
        
    except Exception as e:
        logger.error(f"Error processing measurement message: {e}")


async def get_variable_by_name(variable_name: str) -> Optional[Dict[str, Any]]:
    """Obtener variable desde Django API"""
    global http_client
    
    try:
        response = await http_client.get(
            f"{DJANGO_API_URL}/api/telemetry/variables/",
            params={"name": variable_name}
        )
        response.raise_for_status()
        
        variables = response.json()
        return variables[0] if variables else None
        
    except Exception as e:
        logger.error(f"Error getting variable {variable_name}: {e}")
        return None


async def create_measurement(measurement_data: MeasurementData, variable_id: int):
    """Crear medición en base de datos"""
    global db_pool
    
    try:
        # Determinar tipo de valor y campos a usar
        value_fields = {}
        
        if isinstance(measurement_data.value, (int, float)):
            value_fields['value_numeric'] = measurement_data.value
        elif isinstance(measurement_data.value, bool):
            value_fields['value_boolean'] = measurement_data.value
        elif isinstance(measurement_data.value, str):
            value_fields['value_text'] = measurement_data.value
        else:
            # Para otros tipos, guardar en raw_value
            measurement_data.raw_value['processed_value'] = measurement_data.value
        
        # Insertar medición
        query = """
            INSERT INTO telemetry_measurement 
            (point_id, variable_id, timestamp, value_numeric, value_text, value_boolean,
             raw_value, quality_score, provider, processing_config, days_since_last_connection,
             created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
            ON CONFLICT (point_id, variable_id, timestamp) 
            DO UPDATE SET
                value_numeric = EXCLUDED.value_numeric,
                value_text = EXCLUDED.value_text,
                value_boolean = EXCLUDED.value_boolean,
                raw_value = EXCLUDED.raw_value,
                quality_score = EXCLUDED.quality_score,
                processing_config = EXCLUDED.processing_config,
                updated_at = EXCLUDED.updated_at
        """
        
        now = datetime.now(CHILE_TZ)
        
        await db_pool.execute(
            query,
            measurement_data.point_id,
            variable_id,
            measurement_data.timestamp,
            value_fields.get('value_numeric'),
            value_fields.get('value_text'),
            value_fields.get('value_boolean'),
            json.dumps(measurement_data.raw_value),
            measurement_data.quality_score,
            measurement_data.provider,
            json.dumps(measurement_data.processing_config),
            measurement_data.days_since_last_connection,
            now,
            now
        )
        
    except Exception as e:
        logger.error(f"Error creating measurement: {e}")
        raise


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "service": "SmartHydro Data Processor",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now(CHILE_TZ).isoformat()
    }


@app.get("/health")
async def health_check():
    """Health check"""
    try:
        # Verificar conexiones
        health_status = "healthy"
        services = {}
        
        # Verificar PostgreSQL
        if db_pool:
            try:
                await db_pool.execute("SELECT 1")
                services["postgresql"] = "connected"
            except Exception as e:
                services["postgresql"] = f"error: {e}"
                health_status = "unhealthy"
        else:
            services["postgresql"] = "not_connected"
            health_status = "unhealthy"
        
        # Verificar Kafka
        if kafka_consumer:
            services["kafka"] = "connected"
        else:
            services["kafka"] = "not_connected"
            health_status = "unhealthy"
        
        # Verificar Django API
        if http_client:
            try:
                response = await http_client.get(f"{DJANGO_API_URL}/health/")
                if response.status_code == 200:
                    services["django_api"] = "connected"
                else:
                    services["django_api"] = f"error: {response.status_code}"
                    health_status = "warning"
            except Exception as e:
                services["django_api"] = f"error: {e}"
                health_status = "warning"
        else:
            services["django_api"] = "not_connected"
            health_status = "unhealthy"
        
        return {
            "status": health_status,
            "timestamp": datetime.now(CHILE_TZ).isoformat(),
            "services": services
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }


@app.post("/process/batch")
async def process_batch(batch_data: BatchData, background_tasks: BackgroundTasks):
    """Procesar lote de mediciones"""
    try:
        # Ejecutar en background
        background_tasks.add_task(process_measurement_batch, batch_data)
        
        return {
            "message": f"Batch processing started: {batch_data.batch_id}",
            "batch_id": batch_data.batch_id,
            "measurements_count": len(batch_data.measurements),
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error starting batch processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def process_measurement_batch(batch_data: BatchData):
    """Procesar lote de mediciones"""
    global db_pool
    
    start_time = datetime.now(CHILE_TZ)
    
    try:
        # Crear registro de lote
        batch_id = await create_batch_record(batch_data, start_time)
        
        processed_count = 0
        failed_count = 0
        
        # Procesar cada medición
        for measurement_data in batch_data.measurements:
            try:
                # Obtener variable
                variable = await get_variable_by_name(measurement_data.variable_name)
                if not variable:
                    failed_count += 1
                    continue
                
                # Crear medición
                await create_measurement(measurement_data, variable['id'])
                processed_count += 1
                
            except Exception as e:
                logger.error(f"Error processing measurement in batch: {e}")
                failed_count += 1
        
        # Actualizar registro de lote
        end_time = datetime.now(CHILE_TZ)
        processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
        
        await update_batch_record(
            batch_id, 
            processed_count, 
            failed_count, 
            processing_time_ms,
            'completed'
        )
        
        logger.info(f"Batch {batch_data.batch_id} completed: {processed_count} processed, {failed_count} failed")
        
    except Exception as e:
        logger.error(f"Error processing batch {batch_data.batch_id}: {e}")
        
        # Actualizar estado a fallido
        if 'batch_id' in locals():
            await update_batch_record(batch_id, 0, len(batch_data.measurements), 0, 'failed')


async def create_batch_record(batch_data: BatchData, start_time: datetime) -> int:
    """Crear registro de lote en base de datos"""
    global db_pool
    
    query = """
        INSERT INTO telemetry_measurement_batch 
        (batch_id, provider, frequency, total_measurements, metadata, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id
    """
    
    result = await db_pool.fetchrow(
        query,
        batch_data.batch_id,
        batch_data.provider,
        batch_data.frequency,
        len(batch_data.measurements),
        json.dumps(batch_data.metadata),
        start_time,
        start_time
    )
    
    return result['id']


async def update_batch_record(batch_id: int, processed: int, failed: int, 
                            processing_time_ms: int, status: str):
    """Actualizar registro de lote"""
    global db_pool
    
    query = """
        UPDATE telemetry_measurement_batch 
        SET processed_measurements = $1, failed_measurements = $2,
            processing_time_ms = $3, status = $4, updated_at = $5
        WHERE id = $6
    """
    
    await db_pool.execute(
        query,
        processed,
        failed,
        processing_time_ms,
        status,
        datetime.now(CHILE_TZ),
        batch_id
    )


@app.get("/stats")
async def get_stats():
    """Obtener estadísticas del procesamiento"""
    global db_pool
    
    try:
        # Estadísticas de mediciones
        measurements_query = "SELECT COUNT(*) as total FROM telemetry_measurement"
        measurements_result = await db_pool.fetchrow(measurements_query)
        total_measurements = measurements_result['total']
        
        # Estadísticas de lotes
        batches_query = """
            SELECT 
                COUNT(*) as total_batches,
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_batches,
                COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_batches,
                AVG(processing_time_ms) as avg_processing_time
            FROM telemetry_measurement_batch
        """
        batches_result = await db_pool.fetchrow(batches_query)
        
        # Estadísticas por proveedor
        provider_query = """
            SELECT provider, COUNT(*) as count
            FROM telemetry_measurement
            GROUP BY provider
            ORDER BY count DESC
        """
        provider_results = await db_pool.fetch(provider_query)
        
        return {
            "total_measurements": total_measurements,
            "batches": {
                "total": batches_result['total_batches'],
                "completed": batches_result['completed_batches'],
                "failed": batches_result['failed_batches'],
                "avg_processing_time_ms": batches_result['avg_processing_time']
            },
            "by_provider": {row['provider']: row['count'] for row in provider_results},
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003) 