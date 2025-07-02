"""
Servicio de Cumplimiento
Gestión y envío de datos de cumplimiento regulatorio
"""
import logging
from typing import Dict, Any, Optional
from django.utils import timezone
from datetime import datetime, date, timedelta

from apps.compliance.models import ComplianceSource, ComplianceConfig, ComplianceData
from apps.catchment.models import CatchmentPoint
from services.telemetry import TelemetryService

logger = logging.getLogger(__name__)


class ComplianceService:
    """Servicio para gestión de cumplimiento regulatorio"""
    
    def __init__(self, compliance_config: ComplianceConfig):
        self.compliance_config = compliance_config
        self.catchment_point = compliance_config.catchment_point
        self.source = compliance_config.compliance_source
    
    def prepare_data(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """
        Prepara datos para envío de cumplimiento
        
        Args:
            start_date: Fecha de inicio
            end_date: Fecha de fin
            
        Returns:
            Datos preparados según el esquema requerido
        """
        try:
            # Obtener datos de telemetría
            telemetry_service = TelemetryService(self.catchment_point)
            telemetry_data = telemetry_service.get_data_range(start_date, end_date)
            
            # Transformar según el esquema requerido
            transformed_data = self._transform_to_schema(telemetry_data)
            
            # Validar contra esquema requerido
            self._validate_schema(transformed_data)
            
            return transformed_data
            
        except Exception as e:
            logger.error(f"Error preparando datos de cumplimiento: {e}")
            raise
    
    def send_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Envía datos a la fuente de cumplimiento
        
        Args:
            data: Datos a enviar
            
        Returns:
            Resultado del envío
        """
        try:
            # Enviar según el tipo de fuente
            if self.source.code == 'DGA':
                response = self._send_to_dga(data)
            elif self.source.code == 'SMA':
                response = self._send_to_sma(data)
            else:
                response = self._send_generic(data)
            
            # Registrar envío
            compliance_data = ComplianceData.objects.create(
                compliance_config=self.compliance_config,
                data=data,
                status='SENT',
                response=response,
                sent_at=timezone.now()
            )
            
            logger.info(f"Datos enviados a {self.source.name} para {self.catchment_point.name}")
            
            return {
                'status': 'success',
                'compliance_data_id': compliance_data.id,
                'response': response
            }
            
        except Exception as e:
            logger.error(f"Error enviando datos a {self.source.name}: {e}")
            
            # Registrar error
            ComplianceData.objects.create(
                compliance_config=self.compliance_config,
                data=data,
                status='ERROR',
                response={'error': str(e)},
                sent_at=timezone.now()
            )
            
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _transform_to_schema(self, telemetry_data: list) -> Dict[str, Any]:
        """Transforma datos de telemetría al esquema requerido"""
        schema = self.source.required_schema
        
        # Implementar transformación según esquema
        transformed = {
            'point_id': self.catchment_point.external_id,
            'point_name': self.catchment_point.name,
            'data': []
        }
        
        for data_point in telemetry_data:
            transformed_point = {}
            
            # Mapear campos según esquema
            for field, mapping in schema.get('fields', {}).items():
                if mapping in data_point.data.get('values', {}):
                    transformed_point[field] = data_point.data['values'][mapping]
            
            if transformed_point:
                transformed['data'].append(transformed_point)
        
        return transformed
    
    def _validate_schema(self, data: Dict[str, Any]) -> bool:
        """Valida datos contra esquema requerido"""
        schema = self.source.required_schema
        
        # Validar campos requeridos
        required_fields = schema.get('required', [])
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Campo requerido '{field}' no encontrado")
        
        return True
    
    def _send_to_dga(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Envía datos a DGA"""
        # Implementar envío específico a DGA
        return {
            'sent_to': 'DGA',
            'timestamp': timezone.now().isoformat(),
            'status': 'received'
        }
    
    def _send_to_sma(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Envía datos a SMA"""
        # Implementar envío específico a SMA
        return {
            'sent_to': 'SMA',
            'timestamp': timezone.now().isoformat(),
            'status': 'received'
        }
    
    def _send_generic(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Envío genérico para otras fuentes"""
        return {
            'sent_to': self.source.name,
            'timestamp': timezone.now().isoformat(),
            'status': 'received'
        }


class ComplianceManager:
    """Gestor principal de cumplimiento"""
    
    @staticmethod
    def send_daily_reports() -> Dict[str, Any]:
        """Envía reportes diarios de cumplimiento"""
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        configs = ComplianceConfig.objects.filter(is_active=True)
        
        results = {
            'total': len(configs),
            'success': 0,
            'errors': 0,
            'details': []
        }
        
        for config in configs:
            try:
                service = ComplianceService(config)
                data = service.prepare_data(yesterday, today)
                result = service.send_data(data)
                
                if result['status'] == 'success':
                    results['success'] += 1
                else:
                    results['errors'] += 1
                
                results['details'].append({
                    'config_id': config.id,
                    'point_name': config.catchment_point.name,
                    'source_name': config.compliance_source.name,
                    'result': result
                })
                
            except Exception as e:
                results['errors'] += 1
                results['details'].append({
                    'config_id': config.id,
                    'error': str(e)
                })
        
        logger.info(f"Reportes diarios enviados: {results['success']} exitosos, {results['errors']} errores")
        
        return results
    
    @staticmethod
    def get_compliance_status(catchment_point: CatchmentPoint) -> Dict[str, Any]:
        """Obtiene estado de cumplimiento de un punto"""
        configs = ComplianceConfig.objects.filter(
            catchment_point=catchment_point,
            is_active=True
        )
        
        status = {
            'point_name': catchment_point.name,
            'sources': []
        }
        
        for config in configs:
            # Obtener último envío
            last_data = ComplianceData.objects.filter(
                compliance_config=config
            ).order_by('-sent_at').first()
            
            source_status = {
                'source_name': config.compliance_source.name,
                'source_code': config.compliance_source.code,
                'last_sent': last_data.sent_at if last_data else None,
                'last_status': last_data.status if last_data else 'NO_DATA'
            }
            
            status['sources'].append(source_status)
        
        return status 