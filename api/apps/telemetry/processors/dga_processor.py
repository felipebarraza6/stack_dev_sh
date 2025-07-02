"""
Sistema DGA Mejorado
Procesa y envía datos a la DGA con cola de procesamiento y validaciones
"""
import logging
import json
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from django.db import transaction
from django.core.cache import cache
from django.conf import settings
import aiohttp
import requests

from api.apps.catchment.models import CatchmentPoint, DgaDataConfigCatchment
from .models import TelemetryData
from api.telemetry.config import telemetry_config

logger = logging.getLogger(__name__)


@dataclass
class DgaData:
    """Datos preparados para envío a DGA"""
    catchment_point_id: int
    date_time: datetime
    flow: float
    total: float
    level: float
    device_id: str
    voucher_number: Optional[str] = None
    error_message: Optional[str] = None
    success: bool = True


class DgaQueueProcessor:
    """Procesador de cola DGA con validaciones y reintentos"""
    
    def __init__(self):
        self.queue_key = "dga_queue"
        self.processing_key = "dga_processing"
        self.max_retries = 3
        self.retry_delay = 300  # 5 minutos
        self.batch_size = 50
    
    def add_to_queue(self, telemetry: TelemetryData) -> bool:
        """
        Agregar registro a la cola DGA
        
        Args:
            telemetry: Registro de telemetría a procesar
            
        Returns:
            bool: True si se agregó correctamente
        """
        try:
            # Validar que el punto tenga configuración DGA
            if not self._has_dga_config(telemetry.catchment_point):
                logger.warning(f"Punto {telemetry.catchment_point.id} sin configuración DGA")
                return False
            
            # Crear datos DGA
            dga_data = DgaData(
                catchment_point_id=telemetry.catchment_point.id,
                date_time=telemetry.measurement_time,
                flow=float(telemetry.flow),
                total=float(telemetry.total) if telemetry.total else 0.0,
                level=float(telemetry.water_table),
                device_id=telemetry.catchment_point.device_id,
                voucher_number=telemetry.dga_voucher
            )
            
            # Validar datos antes de agregar a cola
            if not self._validate_dga_data(dga_data):
                logger.warning(f"Datos DGA inválidos para punto {interaction.catchment_point.id}")
                return False
            
            # Agregar a cola Redis
            queue_item = {
                'id': telemetry.id,
                'data': dga_data.__dict__,
                'retries': 0,
                'created_at': datetime.now().isoformat()
            }
            
            cache.lpush(self.queue_key, json.dumps(queue_item, default=str))
            logger.info(f"Agregado a cola DGA: punto {telemetry.catchment_point.id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error agregando a cola DGA: {str(e)}")
            return False
    
    def _has_dga_config(self, catchment_point: CatchmentPoint) -> bool:
        """Verificar si el punto tiene configuración DGA"""
        try:
            return DgaDataConfigCatchment.objects.filter(
                catchment_point=catchment_point
            ).exists()
        except Exception as e:
            logger.error(f"Error verificando configuración DGA: {str(e)}")
            return False
    
    def _validate_dga_data(self, dga_data: DgaData) -> bool:
        """Validar datos antes de enviar a DGA"""
        try:
            # Validar valores requeridos
            if dga_data.flow < 0 or dga_data.total < 0 or dga_data.level < 0:
                return False
            
            # Validar que el caudal no sea 0 si el total es mayor a 0
            if dga_data.flow == 0.0 and dga_data.total > 0.0:
                return False
            
            # Validar que el nivel esté en rango razonable
            if dga_data.level > 100.0:  # Más de 100m es sospechoso
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validando datos DGA: {str(e)}")
            return False
    
    async def process_queue(self):
        """Procesar cola DGA de manera asíncrona"""
        try:
            # Verificar si ya hay procesamiento en curso
            if cache.get(self.processing_key):
                logger.info("Procesamiento DGA ya en curso")
                return
            
            # Marcar como en procesamiento
            cache.set(self.processing_key, True, timeout=300)  # 5 minutos
            
            while True:
                # Obtener lote de elementos de la cola
                batch = []
                for _ in range(self.batch_size):
                    item = cache.rpop(self.queue_key)
                    if item:
                        batch.append(json.loads(item))
                    else:
                        break
                
                if not batch:
                    logger.info("Cola DGA vacía")
                    break
                
                # Procesar lote
                await self._process_batch(batch)
                
                # Pequeña pausa entre lotes
                await asyncio.sleep(1)
            
        except Exception as e:
            logger.error(f"Error procesando cola DGA: {str(e)}")
        finally:
            # Liberar marca de procesamiento
            cache.delete(self.processing_key)
    
    async def _process_batch(self, batch: List[Dict[str, Any]]):
        """Procesar un lote de elementos de la cola"""
        try:
            tasks = []
            for item in batch:
                task = self._process_queue_item(item)
                tasks.append(task)
            
            # Procesar en paralelo
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Manejar resultados
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Error procesando item {batch[i]['id']}: {str(result)}")
                    self._handle_failed_item(batch[i])
                elif not result:
                    self._handle_failed_item(batch[i])
                    
        except Exception as e:
            logger.error(f"Error procesando lote DGA: {str(e)}")
    
    async def _process_queue_item(self, item: Dict[str, Any]) -> bool:
        """Procesar un elemento individual de la cola"""
        try:
            dga_data = DgaData(**item['data'])
            
            # Obtener configuración DGA del punto
            dga_config = DgaDataConfigCatchment.objects.filter(
                catchment_point_id=dga_data.catchment_point_id
            ).first()
            
            if not dga_config:
                logger.error(f"Configuración DGA no encontrada para punto {dga_data.catchment_point_id}")
                return False
            
            # Preparar datos para envío
            payload = self._prepare_dga_payload(dga_data, dga_config)
            
            # Enviar a DGA
            success = await self._send_to_dga(payload, dga_config)
            
            if success:
                # Actualizar registro en base de datos
                await self._update_telemetry_success(item['id'])
                logger.info(f"Datos DGA enviados exitosamente para punto {dga_data.catchment_point_id}")
                return True
            else:
                logger.error(f"Error enviando datos DGA para punto {dga_data.catchment_point_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error procesando item DGA: {str(e)}")
            return False
    
    def _prepare_dga_payload(self, dga_data: DgaData, 
                           dga_config: DgaDataConfigCatchment) -> Dict[str, Any]:
        """Preparar payload para envío a DGA"""
        try:
            return {
                'codigo_componente': dga_config.codigo_componente,
                'fecha_medicion': dga_data.date_time.strftime('%Y-%m-%d %H:%M:%S'),
                'caudal': round(dga_data.flow, 2),
                'acumulado': round(dga_data.total, 2),
                'nivel_freatico': round(dga_data.level, 2),
                'dispositivo_id': dga_data.device_id,
                'numero_comprobante': dga_data.voucher_number or '',
                'configuracion_id': dga_config.id
            }
        except Exception as e:
            logger.error(f"Error preparando payload DGA: {str(e)}")
            return {}
    
    async def _send_to_dga(self, payload: Dict[str, Any], 
                          dga_config: DgaDataConfigCatchment) -> bool:
        """Enviar datos a la API de DGA"""
        try:
            # Configurar timeout y reintentos
            timeout = aiohttp.ClientTimeout(total=30)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    url=dga_config.api_endpoint,
                    json=payload,
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f"Bearer {dga_config.api_key}"
                    }
                ) as response:
                    
                    if response.status == 200:
                        response_data = await response.json()
                        logger.info(f"Respuesta DGA: {response_data}")
                        return True
                    else:
                        logger.error(f"Error HTTP {response.status} en DGA")
                        return False
                        
        except Exception as e:
            logger.error(f"Error enviando a DGA: {str(e)}")
            return False
    
    async def _update_telemetry_success(self, telemetry_id: int):
        """Actualizar registro de telemetría como enviado exitosamente"""
        try:
            with transaction.atomic():
                telemetry = TelemetryData.objects.get(id=telemetry_id)
                telemetry.send_dga = True
                telemetry.dga_response = "Enviado exitosamente"
                telemetry.save()
                
        except Exception as e:
            logger.error(f"Error actualizando telemetría {telemetry_id}: {str(e)}")
    
    def _handle_failed_item(self, item: Dict[str, Any]):
        """Manejar elemento fallido de la cola"""
        try:
            retries = item.get('retries', 0)
            
            if retries < self.max_retries:
                # Reintentar
                item['retries'] = retries + 1
                item['last_retry'] = datetime.now().isoformat()
                
                # Agregar de vuelta a la cola con delay
                cache.lpush(self.queue_key, json.dumps(item, default=str))
                logger.info(f"Reintentando item {item['id']} (intento {retries + 1})")
            else:
                # Marcar como fallido permanentemente
                logger.error(f"Item {item['id']} falló después de {self.max_retries} intentos")
                self._mark_as_failed(item)
                
        except Exception as e:
            logger.error(f"Error manejando item fallido: {str(e)}")
    
    def _mark_as_failed(self, item: Dict[str, Any]):
        """Marcar elemento como fallido permanentemente"""
        try:
            with transaction.atomic():
                telemetry = TelemetryData.objects.get(id=item['id'])
                telemetry.send_dga = False
                telemetry.dga_response = f"Error después de {self.max_retries} intentos"
                telemetry.is_error = True
                telemetry.save()
                
        except Exception as e:
            logger.error(f"Error marcando item como fallido: {str(e)}")
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Obtener estado de la cola DGA"""
        try:
            queue_length = cache.llen(self.queue_key)
            is_processing = bool(cache.get(self.processing_key))
            
            return {
                'queue_length': queue_length,
                'is_processing': is_processing,
                'max_retries': self.max_retries,
                'batch_size': self.batch_size,
                'last_check': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo estado de cola: {str(e)}")
            return {}
    
    def clear_queue(self) -> bool:
        """Limpiar cola DGA (solo para emergencias)"""
        try:
            cache.delete(self.queue_key)
            cache.delete(self.processing_key)
            logger.warning("Cola DGA limpiada manualmente")
            return True
        except Exception as e:
            logger.error(f"Error limpiando cola: {str(e)}")
            return False


# Instancia global del procesador DGA
dga_processor = DgaQueueProcessor() 