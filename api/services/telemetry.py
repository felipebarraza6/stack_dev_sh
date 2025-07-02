"""
Servicio de Telemetría
Procesamiento y gestión de datos de telemetría
"""
import logging
from typing import Dict, Any, Optional
from django.utils import timezone

from apps.catchment.models import CatchmentPoint
from apps.telemetry.models import TelemetryData

logger = logging.getLogger(__name__)


class TelemetryService:
    """Servicio para procesamiento de telemetría"""
    
    def __init__(self, catchment_point: CatchmentPoint):
        self.catchment_point = catchment_point
    
    def process_data(self, data: Dict[str, Any], source: str = 'mqtt') -> Dict[str, Any]:
        """
        Procesa datos de telemetría
        
        Args:
            data: Datos a procesar
            source: Fuente de los datos
            
        Returns:
            Resultado del procesamiento
        """
        try:
            # Validar datos
            validated_data = self._validate_data(data)
            
            # Procesar según el tipo de punto de captación
            processed_data = self._process_by_type(validated_data)
            
            # Guardar datos procesados
            telemetry_data = TelemetryData.objects.create(
                catchment_point=self.catchment_point,
                data=processed_data,
                source=source,
                processed_at=timezone.now()
            )
            
            logger.info(f"Datos procesados para {self.catchment_point.name}: {len(processed_data)} registros")
            
            return {
                'status': 'success',
                'data_id': telemetry_data.id,
                'processed_records': len(processed_data)
            }
            
        except Exception as e:
            logger.error(f"Error procesando datos para {self.catchment_point.name}: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida los datos de entrada"""
        required_fields = ['timestamp', 'values']
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Campo requerido '{field}' no encontrado")
        
        return data
    
    def _process_by_type(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Procesa datos según el tipo de punto de captación"""
        point_type = self.catchment_point.point_type
        
        if point_type == 'FLOW':
            return self._process_flow_data(data)
        elif point_type == 'LEVEL':
            return self._process_level_data(data)
        elif point_type == 'QUALITY':
            return self._process_quality_data(data)
        else:
            return data
    
    def _process_flow_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Procesa datos de flujo"""
        processed = data.copy()
        
        # Aplicar factores de corrección
        if 'flow_rate' in data['values']:
            processed['values']['flow_rate'] = data['values']['flow_rate'] * 1.1
        
        return processed
    
    def _process_level_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Procesa datos de nivel"""
        processed = data.copy()
        
        # Aplicar corrección de presión atmosférica
        if 'water_level' in data['values']:
            processed['values']['water_level'] = data['values']['water_level'] + 0.5
        
        return processed
    
    def _process_quality_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Procesa datos de calidad"""
        processed = data.copy()
        
        # Aplicar filtros de calidad
        if 'temperature' in data['values']:
            temp = data['values']['temperature']
            if temp < -10 or temp > 50:
                processed['values']['temperature'] = None
        
        return processed
    
    def get_latest_data(self) -> Optional[TelemetryData]:
        """Obtiene los datos más recientes"""
        return TelemetryData.objects.filter(
            catchment_point=self.catchment_point
        ).order_by('-processed_at').first()
    
    def get_data_range(self, start_date, end_date) -> list:
        """Obtiene datos en un rango de fechas"""
        return TelemetryData.objects.filter(
            catchment_point=self.catchment_point,
            processed_at__range=(start_date, end_date)
        ).order_by('processed_at')


class TelemetryProcessor:
    """Procesador principal de telemetría"""
    
    @staticmethod
    def process_batch(catchment_points: list, data_source: str = 'mqtt') -> Dict[str, Any]:
        """
        Procesa datos para múltiples puntos de captación
        
        Args:
            catchment_points: Lista de puntos de captación
            data_source: Fuente de datos
            
        Returns:
            Resultado del procesamiento por lotes
        """
        results = {
            'success': 0,
            'errors': 0,
            'details': []
        }
        
        for point in catchment_points:
            service = TelemetryService(point)
            result = service.process_data({}, data_source)
            
            if result['status'] == 'success':
                results['success'] += 1
            else:
                results['errors'] += 1
            
            results['details'].append({
                'point_id': point.id,
                'point_name': point.name,
                'result': result
            })
        
        logger.info(f"Procesamiento por lotes completado: {results['success']} exitosos, {results['errors']} errores")
        
        return results 