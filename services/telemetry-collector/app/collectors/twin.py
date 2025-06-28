"""
Twin (TData) Collector
Migra la lógica de api/cronjobs/telemetry/twin.py, twin_f1.py, twin_f5.py
"""
import httpx
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import pytz
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Zona horaria de Chile
CHILE_TZ = pytz.timezone('America/Santiago')

class TwinMeasurement(BaseModel):
    """Modelo para mediciones de Twin"""
    point_id: int
    date_time_medition: datetime
    total: Optional[float] = None
    flow: Optional[float] = None
    water_table: Optional[float] = None
    level: Optional[float] = None
    pulses: Optional[int] = None
    days_not_conection: Optional[int] = 0
    send_dga: bool = False
    provider: str = "twin"

class TwinCollector:
    """Colector de datos para proveedor Twin (TData)"""
    
    def __init__(self, django_api_url: str, kafka_producer=None):
        self.django_api_url = django_api_url
        self.kafka_producer = kafka_producer
        self.provider_name = "twin"
    
    async def collect_by_frequency(self, frequency: str) -> List[TwinMeasurement]:
        """
        Recolectar datos para una frecuencia específica
        Migra la lógica de twin.py, twin_f1.py, twin_f5.py
        """
        logger.info(f"Starting Twin collection for frequency: {frequency}")
        
        try:
            # 1. Obtener puntos de captación desde Django
            points = await self._get_catchment_points(frequency)
            
            if not points:
                logger.info(f"No points found for Twin frequency {frequency}")
                return []
            
            measurements = []
            
            # 2. Procesar cada punto
            for point in points:
                try:
                    measurement = await self._collect_point_data(point, frequency)
                    if measurement:
                        measurements.append(measurement)
                        
                except Exception as e:
                    logger.error(f"Error collecting data for point {point.get('id')}: {e}")
                    continue
            
            logger.info(f"Twin collection completed: {len(measurements)} measurements")
            return measurements
            
        except Exception as e:
            logger.error(f"Error in Twin collection: {e}")
            return []
    
    async def _get_catchment_points(self, frequency: str) -> List[Dict[str, Any]]:
        """Obtener puntos de captación desde Django API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.django_api_url}/api/catchment-points/",
                    params={
                        "is_tdata": True,
                        "is_telemetry": True,
                        "frecuency": frequency
                    },
                    timeout=10
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Error getting catchment points: {e}")
            return []
    
    async def _collect_point_data(self, point: Dict[str, Any], frequency: str) -> Optional[TwinMeasurement]:
        """Recolectar datos de un punto específico"""
        point_id = point.get('id')
        logger.info(f"Collecting Twin data for point {point_id}")
        
        try:
            # Obtener configuración del punto
            profile_config = point.get('profile_data_config', {})
            
            if not self._validate_profile_config(profile_config):
                logger.warning(f"Invalid profile config for point {point_id}")
                return None
            
            # Obtener datos del proveedor Twin
            raw_data = await self._get_twin_data(point, profile_config)
            
            if not raw_data:
                logger.warning(f"No data received for point {point_id}")
                return None
            
            # Procesar datos
            measurement = await self._process_twin_data(point, raw_data, frequency)
            
            # Enviar a Kafka si está disponible
            if self.kafka_producer and measurement:
                await self._send_to_kafka(measurement)
            
            return measurement
            
        except Exception as e:
            logger.error(f"Error collecting point data for {point_id}: {e}")
            return None
    
    def _validate_profile_config(self, profile_config: Dict[str, Any]) -> bool:
        """Validar configuración del perfil"""
        required_keys = ['scheme', 'token_service']
        
        if not all(key in profile_config for key in required_keys):
            return False
        
        scheme = profile_config.get('scheme', {})
        if 'variables' not in scheme:
            return False
        
        return True
    
    async def _get_twin_data(self, point: Dict[str, Any], profile_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Obtener datos del proveedor Twin
        Migra la lógica de getters/tdata.py
        """
        try:
            # TODO: Implementar llamada real a Twin API
            # Por ahora simulamos datos
            token = profile_config.get('token_service')
            variables = profile_config.get('scheme', {}).get('variables', {})
            
            logger.info(f"Getting Twin data with token: {token[:10]}...")
            
            # Simulación de datos
            return {
                'total': 1234.56,
                'flow': 45.67,
                'water_table': 12.34,
                'level': 5.67,
                'pulses': 100,
                'date_time_medition': datetime.now(CHILE_TZ).isoformat(),
                'date_time_last_logger': datetime.now(CHILE_TZ).isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting Twin data: {e}")
            return None
    
    async def _process_twin_data(self, point: Dict[str, Any], raw_data: Dict[str, Any], frequency: str) -> Optional[TwinMeasurement]:
        """
        Procesar datos de Twin
        Migra la lógica de controllers/
        """
        try:
            point_id = point.get('id')
            
            # Calcular días sin conexión
            days_not_conection = 0
            if raw_data.get('date_time_last_logger'):
                try:
                    date_medition = datetime.fromisoformat(raw_data['date_time_medition'].replace('Z', '+00:00'))
                    date_last_logger = datetime.fromisoformat(raw_data['date_time_last_logger'].replace('Z', '+00:00'))
                    days_not_conection = max((date_medition - date_last_logger).days, 0)
                except Exception as e:
                    logger.warning(f"Error calculating days not connection: {e}")
            
            # Determinar si enviar a DGA
            send_dga = await self._should_send_to_dga(point, frequency)
            
            # Crear medición
            measurement = TwinMeasurement(
                point_id=point_id,
                date_time_medition=datetime.fromisoformat(raw_data['date_time_medition'].replace('Z', '+00:00')),
                total=raw_data.get('total'),
                flow=raw_data.get('flow'),
                water_table=raw_data.get('water_table'),
                level=raw_data.get('level'),
                pulses=raw_data.get('pulses'),
                days_not_conection=days_not_conection,
                send_dga=send_dga,
                provider=self.provider_name
            )
            
            logger.info(f"Processed Twin data for point {point_id}: {measurement}")
            return measurement
            
        except Exception as e:
            logger.error(f"Error processing Twin data: {e}")
            return None
    
    async def _should_send_to_dga(self, point: Dict[str, Any], frequency: str) -> bool:
        """
        Determinar si enviar datos a DGA
        Migra la lógica de verificación DGA
        """
        try:
            # Obtener configuración DGA desde Django
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.django_api_url}/api/dga-config/{point.get('id')}/",
                    timeout=5
                )
                if response.status_code == 200:
                    dga_config = response.json()
                    
                    # Lógica de envío según estándar
                    standard = dga_config.get('standard', 'SIN_ESTANDAR')
                    
                    if standard == "MAYOR":
                        return dga_config.get('send_dga', False)
                    
                    elif standard == "MEDIO":
                        # Verificar si ya se envió hoy
                        today = datetime.now(CHILE_TZ).strftime("%Y-%m-%d")
                        # TODO: Verificar en base de datos si ya se envió hoy
                        return dga_config.get('send_dga', False)
                    
                    elif standard in ["MENOR", "CAUDALES_MUY_PEQUENOS"]:
                        return dga_config.get('send_dga', False)
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking DGA send condition: {e}")
            return False
    
    async def _send_to_kafka(self, measurement: TwinMeasurement):
        """Enviar medición a Kafka"""
        try:
            if self.kafka_producer:
                topic = "measurements"
                message = measurement.dict()
                await self.kafka_producer.send(topic, message)
                logger.info(f"Sent measurement to Kafka: {measurement.point_id}")
        except Exception as e:
            logger.error(f"Error sending to Kafka: {e}")

# Función de conveniencia para usar desde el scheduler
async def collect_twin_data(frequency: str, django_api_url: str, kafka_producer=None):
    """Función para usar desde Celery scheduler"""
    collector = TwinCollector(django_api_url, kafka_producer)
    return await collector.collect_by_frequency(frequency) 