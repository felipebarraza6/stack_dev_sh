"""
Procesador DGA optimizado
Migra la lógica de api/cronjobs/dga/ a FastAPI
"""
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import pytz
import httpx
import xml.etree.ElementTree as ET
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Zona horaria de Chile
CHILE_TZ = pytz.timezone('America/Santiago')

class DgaData(BaseModel):
    """Modelo para datos DGA"""
    catchment_point_id: int
    catchment_point_title: str
    date_time_medition: datetime
    total: Optional[float] = None
    flow: Optional[float] = None
    water_table: Optional[float] = None
    code_dga: str
    type_dga: str
    rut: str
    password: str
    interaction_id: int

class DgaProcessor:
    """Procesador para envío de datos a DGA"""
    
    def __init__(self):
        self.dga_url = "https://snia.mop.gob.cl/controlextraccion/datosExtraccion/SendDataExtraccionService"
        self.headers = {
            'Content-Type': 'application/xml',
            'User-Agent': 'SmartHydro-DGA-Client/2.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-CL,es;q=0.9,en;q=0.8',
            'Connection': 'keep-alive'
        }
    
    async def get_pending_dga_data(self, limit: int = 10) -> List[DgaData]:
        """
        Obtiene datos pendientes de envío a DGA
        Migra la lógica de cron_dga.py
        """
        try:
            # TODO: Conectar a base de datos PostgreSQL
            # Por ahora simulamos la consulta
            logger.info(f"Obteniendo {limit} registros pendientes de DGA")
            
            # Simular datos de prueba
            pending_data = []
            for i in range(limit):
                data = DgaData(
                    catchment_point_id=123 + i,
                    catchment_point_title=f"Pozo Test {i+1}",
                    date_time_medition=datetime.now(CHILE_TZ),
                    total=1000.0 + i * 100,
                    flow=12.5 + i * 0.5,
                    water_table=2.1 + i * 0.1,
                    code_dga="BOR001",
                    type_dga="SUBTERRANEO",
                    rut="12345678-9",
                    password="test_password",
                    interaction_id=1000 + i
                )
                pending_data.append(data)
            
            return pending_data
            
        except Exception as e:
            logger.error(f"Error obteniendo datos pendientes DGA: {e}")
            return []
    
    def _convert_to_int(self, value: Any, catchment_point_id: int = None) -> int:
        """
        Convierte valor a entero con validaciones especiales
        Migra la lógica de convertir_a_int()
        """
        try:
            # Caso especial para punto 83 (suma de puntos 83, 84, 85)
            if catchment_point_id == 83:
                # TODO: Implementar suma de múltiples puntos
                logger.info("Procesando suma especial para punto 83")
                return int(float(value))
            
            return int(float(value))
        except (ValueError, TypeError):
            return 0
    
    def _format_dga_payload(self, data: DgaData) -> str:
        """
        Formatea payload para envío DGA
        Migra la lógica de send_data_dga.py
        """
        # Convertir datetime a zona horaria de Chile
        date_time_chile = data.date_time_medition.astimezone(CHILE_TZ)
        time_stamp_origen = date_time_chile.strftime("%Y-%m-%dT%H:%M:%S") + 'Z'
        fecha_medicion = date_time_chile.strftime("%d-%m-%Y")
        hora_medicion = date_time_chile.strftime("%H:%M:%S")
        
        # Procesar valores
        totalizador = self._convert_to_int(data.total, data.catchment_point_id)
        caudal = max(0.0, data.flow or 0.0)
        nivel_freatico = max(0.0, data.water_table or 0.0)
        
        logger.info(f"Formateando datos DGA: {data.catchment_point_title} - {fecha_medicion} {hora_medicion}")
        
        # Determinar tipo de payload según type_dga
        if data.type_dga == 'SUBTERRANEO':
            return self._create_subterraneo_payload(
                data.code_dga, time_stamp_origen, data.rut, data.password,
                fecha_medicion, hora_medicion, totalizador, caudal, nivel_freatico
            )
        else:
            return self._create_superficial_payload(
                data.code_dga, time_stamp_origen, data.rut, data.password,
                fecha_medicion, hora_medicion, totalizador, caudal
            )
    
    def _create_subterraneo_payload(self, codigo_obra: str, time_stamp: str, 
                                  rut: str, password: str, fecha: str, hora: str,
                                  totalizador: int, caudal: float, nivel: float) -> str:
        """Crea payload para extracción subterránea"""
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:aut="http://www.mop.cl/controlextraccion/xsd/datosExtraccion/AuthSendDataExtraccionRequest">
            <soapenv:Header>
                <aut:authSendDataExtraccionTraza>
                    <aut:codigoDeLaObra>{codigo_obra}</aut:codigoDeLaObra>
                    <aut:timeStampOrigen>{time_stamp}</aut:timeStampOrigen>
                </aut:authSendDataExtraccionTraza>
            </soapenv:Header>
            <soapenv:Body>
                <aut:authSendDataExtraccionRequest>
                    <aut:authDataUsuario>
                        <aut:idUsuario>
                            <aut:rut>{rut}</aut:rut>
                        </aut:idUsuario>
                        <aut:password>{password}</aut:password>
                    </aut:authDataUsuario>
                    <aut:authDataExtraccionSubterranea>
                        <aut:fechaMedicion>{fecha}</aut:fechaMedicion>
                        <aut:horaMedicion>{hora}</aut:horaMedicion>
                        <aut:totalizador>{totalizador}</aut:totalizador>
                        <aut:caudal>{caudal}</aut:caudal>
                        <aut:nivelFreaticoDelPozo>{nivel}</aut:nivelFreaticoDelPozo>
                    </aut:authDataExtraccionSubterranea>
                </aut:authSendDataExtraccionRequest>
            </soapenv:Body>
        </soapenv:Envelope>
        """
    
    def _create_superficial_payload(self, codigo_obra: str, time_stamp: str,
                                  rut: str, password: str, fecha: str, hora: str,
                                  totalizador: int, caudal: float) -> str:
        """Crea payload para extracción superficial"""
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:aut="http://www.mop.cl/controlextraccion/xsd/datosExtraccion/AuthSendDataExtraccionRequest">
            <soapenv:Header>
                <aut:authSendDataExtraccionTraza>
                    <aut:codigoDeLaObra>{codigo_obra}</aut:codigoDeLaObra>
                    <aut:timeStampOrigen>{time_stamp}</aut:timeStampOrigen>
                </aut:authSendDataExtraccionTraza>
            </soapenv:Header>
            <soapenv:Body>
                <aut:authSendDataExtraccionRequest>
                    <aut:authDataUsuario>
                        <aut:idUsuario>
                            <aut:rut>{rut}</aut:rut>
                        </aut:idUsuario>
                        <aut:password>{password}</aut:password>
                    </aut:authDataUsuario>
                    <aut:authDataExtraccionSuperficial>
                        <aut:fechaMedicion>{fecha}</aut:fechaMedicion>
                        <aut:horaMedicion>{hora}</aut:horaMedicion>
                        <aut:totalizador>{totalizador}</aut:totalizador>
                        <aut:caudal>{caudal}</aut:caudal>
                    </aut:authDataExtraccionSuperficial>
                </aut:authSendDataExtraccionRequest>
            </soapenv:Body>
        </soapenv:Envelope>
        """
    
    async def send_to_dga(self, data: DgaData) -> Dict[str, Any]:
        """
        Envía datos a DGA con reintentos
        Migra la lógica de send() con mejoras
        """
        payload = self._format_dga_payload(data)
        
        for attempt in range(3):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        self.dga_url,
                        headers=self.headers,
                        content=payload
                    )
                    
                    logger.info(f"Respuesta DGA (intento {attempt + 1}): {response.status_code}")
                    
                    # Verificar si la respuesta es HTML (error)
                    if response.headers.get('content-type', '').startswith('text/html'):
                        logger.error("Error: Servidor DGA no responde correctamente")
                        return {
                            'success': False,
                            'error': 'Servidor DGA no responde correctamente',
                            'attempt': attempt + 1
                        }
                    
                    # Procesar respuesta XML
                    return await self._process_dga_response(response.text, data.interaction_id)
                    
            except httpx.RequestError as e:
                logger.error(f"Error de conexión DGA (intento {attempt + 1}): {e}")
                if attempt < 2:
                    await asyncio.sleep(10)  # Esperar antes de reintentar
                else:
                    return {
                        'success': False,
                        'error': f'Error de conexión: {str(e)}',
                        'attempt': attempt + 1
                    }
            except Exception as e:
                logger.error(f"Error inesperado DGA (intento {attempt + 1}): {e}")
                return {
                    'success': False,
                    'error': f'Error inesperado: {str(e)}',
                    'attempt': attempt + 1
                }
        
        return {
            'success': False,
            'error': 'Fallaron todos los intentos de envío',
            'attempt': 3
        }
    
    async def _process_dga_response(self, response_text: str, interaction_id: int) -> Dict[str, Any]:
        """
        Procesa respuesta XML de DGA
        Migra la lógica de procesamiento de respuesta
        """
        try:
            # Limpiar respuesta
            cleaned_response = response_text.encode('ascii', 'ignore').decode('ascii')
            root = ET.fromstring(cleaned_response)
            
            # Extraer elementos de respuesta
            namespace = '{http://www.mop.cl/controlextraccion/xsd/datosExtraccion/AuthSendDataExtraccionResponse}'
            
            numero_comprobante = root.find(f'.//{namespace}numeroComprobante')
            code = root.find(f'.//{namespace}Code')
            description = root.find(f'.//{namespace}Description')
            
            code_value = code.text if code is not None else '999'
            description_text = description.text if description is not None else 'Sin descripción'
            
            is_success = code_value == '0'
            is_error = not is_success
            
            result = {
                'success': is_success,
                'code': code_value,
                'description': f"({code_value}) {description_text}",
                'numero_comprobante': numero_comprobante.text if numero_comprobante is not None else None,
                'interaction_id': interaction_id,
                'is_error': is_error
            }
            
            logger.info(f"Procesada respuesta DGA: {result}")
            return result
            
        except ET.ParseError as e:
            logger.error(f"Error parseando respuesta XML DGA: {e}")
            return {
                'success': False,
                'error': f'Error parseando respuesta: {str(e)}',
                'interaction_id': interaction_id
            }
    
    async def process_dga_queue(self, limit: int = 10) -> Dict[str, Any]:
        """
        Procesa cola de datos DGA
        Método principal para procesar datos pendientes
        """
        try:
            logger.info(f"Iniciando procesamiento de cola DGA (límite: {limit})")
            
            # Obtener datos pendientes
            pending_data = await self.get_pending_dga_data(limit)
            
            if not pending_data:
                logger.info("No hay datos pendientes de DGA")
                return {
                    'processed': 0,
                    'success': 0,
                    'errors': 0,
                    'details': []
                }
            
            results = []
            success_count = 0
            error_count = 0
            
            for data in pending_data:
                logger.info(f"Procesando DGA para punto {data.catchment_point_id}")
                
                result = await self.send_to_dga(data)
                results.append(result)
                
                if result.get('success', False):
                    success_count += 1
                    # Esperar entre envíos exitosos
                    await asyncio.sleep(20)
                else:
                    error_count += 1
                
                # TODO: Actualizar base de datos con resultado
            
            logger.info(f"Procesamiento DGA completado: {success_count} exitosos, {error_count} errores")
            
            return {
                'processed': len(pending_data),
                'success': success_count,
                'errors': error_count,
                'details': results
            }
            
        except Exception as e:
            logger.error(f"Error en procesamiento de cola DGA: {e}")
            return {
                'processed': 0,
                'success': 0,
                'errors': 1,
                'error': str(e)
            } 