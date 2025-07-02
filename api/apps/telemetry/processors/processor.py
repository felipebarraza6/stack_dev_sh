"""
Procesador Inteligente de Telemetría
Maneja las reglas específicas de procesamiento para cada variable
"""
import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from django.db import transaction
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings

from api.apps.catchment.models import CatchmentPoint, NotificationsCatchment
from .models import TelemetryData
from api.telemetry.config import telemetry_config, ProcessingRule, VariableType

logger = logging.getLogger(__name__)


@dataclass
class ProcessedData:
    """Datos procesados con validaciones aplicadas"""
    flow: float = 0.0
    total: float = 0.0
    level: float = 0.0
    pulses: int = 0
    is_valid: bool = True
    alerts: List[str] = None
    resets: List[str] = None
    
    def __post_init__(self):
        if self.alerts is None:
            self.alerts = []
        if self.resets is None:
            self.resets = []


class TelemetryProcessor:
    """Procesador inteligente para datos de telemetría"""
    
    def __init__(self):
        self.config = telemetry_config
        self.cache_ttl = 3600  # 1 hora
    
    def process_catchment_point_data(self, catchment_point: CatchmentPoint, 
                                   raw_data: Dict[str, Any]) -> ProcessedData:
        """
        Procesa los datos de un punto de captación aplicando todas las reglas
        
        Args:
            catchment_point: Punto de captación
            raw_data: Datos crudos del proveedor
            
        Returns:
            ProcessedData: Datos procesados con validaciones
        """
        try:
            # Extraer datos básicos
            processed_data = ProcessedData(
                flow=float(raw_data.get('flow', 0.0)),
                total=float(raw_data.get('total', 0.0)),
                level=float(raw_data.get('level', 0.0)),
                pulses=int(raw_data.get('pulses', 0))
            )
            
            # Aplicar reglas de procesamiento específicas
            self._apply_processing_rules(catchment_point, processed_data, raw_data)
            
            # Validar consistencia entre variables
            self._validate_variable_consistency(catchment_point, processed_data)
            
            # Generar alertas si es necesario
            self._generate_alerts(catchment_point, processed_data)
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error procesando datos para punto {catchment_point.id}: {str(e)}")
            return ProcessedData(is_valid=False, alerts=[f"Error de procesamiento: {str(e)}"])
    
    def _apply_processing_rules(self, catchment_point: CatchmentPoint, 
                               processed_data: ProcessedData, raw_data: Dict[str, Any]):
        """Aplicar reglas de procesamiento específicas para cada variable"""
        
        # Regla 1: Resetear total cuando llega a 0
        if self._should_reset_total(processed_data, raw_data):
            processed_data.total = 0.0
            processed_data.resets.append("Total reseteado a 0")
            logger.info(f"Total reseteado para punto {catchment_point.id}")
        
        # Regla 2: Resetear nivel cuando supera máximo
        if self._should_reset_level(processed_data):
            processed_data.level = 0.0
            processed_data.resets.append("Nivel reseteado por superar máximo")
            logger.info(f"Nivel reseteado para punto {catchment_point.id}")
        
        # Regla 3: Validar consistencia caudal-total
        if self._should_reset_flow_total_inconsistency(processed_data, raw_data):
            processed_data.flow = 0.0
            processed_data.resets.append("Caudal reseteado por inconsistencia con total")
            logger.warning(f"Inconsistencia caudal-total detectada en punto {catchment_point.id}")
        
        # Regla 4: Validar consistencia nivel-acumulado
        if self._should_reset_level_accumulated_inconsistency(processed_data, raw_data):
            processed_data.level = 0.0
            processed_data.resets.append("Nivel reseteado por inconsistencia con acumulado")
            logger.warning(f"Inconsistencia nivel-acumulado detectada en punto {catchment_point.id}")
    
    def _should_reset_total(self, processed_data: ProcessedData, raw_data: Dict[str, Any]) -> bool:
        """Determinar si el total debe ser reseteado"""
        # Si el total llega a 0 y el caudal no es 0, resetear
        if processed_data.total == 0.0 and processed_data.flow > 0.0:
            return True
        
        # Si el total es menor que el anterior (posible reset del contador)
        previous_total = self._get_previous_total(raw_data.get('device_id'))
        if previous_total and processed_data.total < previous_total:
            return True
        
        return False
    
    def _should_reset_level(self, processed_data: ProcessedData) -> bool:
        """Determinar si el nivel debe ser reseteado"""
        # Si el nivel supera el máximo configurado
        level_config = self.config.get_variable_config('level')
        if level_config and level_config.reset_threshold:
            return processed_data.level >= level_config.reset_threshold
        
        return False
    
    def _should_reset_flow_total_inconsistency(self, processed_data: ProcessedData, 
                                             raw_data: Dict[str, Any]) -> bool:
        """Detectar inconsistencia entre caudal y total"""
        # Si hay caudal pero el total no aumenta proporcionalmente
        if processed_data.flow > 0.0:
            previous_total = self._get_previous_total(raw_data.get('device_id'))
            if previous_total:
                expected_increase = processed_data.flow * 0.001  # Conversión l/s a m³
                actual_increase = processed_data.total - previous_total
                
                # Si el total no aumenta cuando debería
                if actual_increase <= 0 and processed_data.flow > 1.0:
                    return True
        
        return False
    
    def _should_reset_level_accumulated_inconsistency(self, processed_data: ProcessedData, 
                                                    raw_data: Dict[str, Any]) -> bool:
        """Detectar inconsistencia entre nivel y acumulado"""
        # Si el nivel cambia significativamente pero el acumulado no
        previous_level = self._get_previous_level(raw_data.get('device_id'))
        if previous_level:
            level_change = abs(processed_data.level - previous_level)
            
            # Si el nivel cambia más de 1m pero el acumulado no cambia
            if level_change > 1.0 and processed_data.total == 0.0:
                return True
        
        return False
    
    def _validate_variable_consistency(self, catchment_point: CatchmentPoint, 
                                     processed_data: ProcessedData):
        """Validar consistencia general entre variables"""
        # Validar que los valores estén dentro de rangos razonables
        for var_name, value in [
            ('flow', processed_data.flow),
            ('total', processed_data.total),
            ('level', processed_data.level),
            ('pulses', processed_data.pulses)
        ]:
            if not self.config.validate_variable_data(var_name, value):
                processed_data.is_valid = False
                processed_data.alerts.append(f"Valor fuera de rango para {var_name}: {value}")
    
    def _generate_alerts(self, catchment_point: CatchmentPoint, processed_data: ProcessedData):
        """Generar alertas basadas en los datos procesados"""
        
        # Alerta si caudal es 0 (posible falla)
        if processed_data.flow == 0.0:
            processed_data.alerts.append("Caudal en 0 - posible falla del sensor")
        
        # Alerta si nivel supera umbral
        level_config = self.config.get_variable_config('level')
        if level_config and level_config.alert_threshold:
            if processed_data.level >= level_config.alert_threshold:
                processed_data.alerts.append(f"Nivel crítico: {processed_data.level}m")
        
        # Alerta si hay resets
        if processed_data.resets:
            processed_data.alerts.extend([f"Reset detectado: {reset}" for reset in processed_data.resets])
    
    def _get_previous_total(self, device_id: str) -> Optional[float]:
        """Obtener el total anterior desde caché o base de datos"""
        cache_key = f"previous_total_{device_id}"
        cached_value = cache.get(cache_key)
        
        if cached_value is not None:
            return cached_value
        
        # Si no está en caché, buscar en la base de datos
        try:
            latest_record = TelemetryData.objects.filter(
                catchment_point__device_id=device_id
            ).order_by('-measurement_time').first()
            
            if latest_record:
                previous_total = float(latest_record.total) if latest_record.total else 0.0
                cache.set(cache_key, previous_total, self.cache_ttl)
                return previous_total
        except Exception as e:
            logger.error(f"Error obteniendo total anterior para {device_id}: {str(e)}")
        
        return None
    
    def _get_previous_level(self, device_id: str) -> Optional[float]:
        """Obtener el nivel anterior desde caché o base de datos"""
        cache_key = f"previous_level_{device_id}"
        cached_value = cache.get(cache_key)
        
        if cached_value is not None:
            return cached_value
        
        try:
            latest_record = TelemetryData.objects.filter(
                catchment_point__device_id=device_id
            ).order_by('-measurement_time').first()
            
            if latest_record:
                previous_level = float(latest_record.water_table) if latest_record.water_table else 0.0
                cache.set(cache_key, previous_level, self.cache_ttl)
                return previous_level
        except Exception as e:
            logger.error(f"Error obteniendo nivel anterior para {device_id}: {str(e)}")
        
        return None
    
    def save_processed_data(self, catchment_point: CatchmentPoint, 
                          processed_data: ProcessedData, 
                          raw_data: Dict[str, Any]) -> TelemetryData:
        """Guardar datos procesados en la base de datos"""
        
        with transaction.atomic():
            # Crear registro de telemetría
            telemetry = TelemetryData.objects.create(
                catchment_point=catchment_point,
                measurement_time=raw_data.get('timestamp', datetime.now()),
                logger_time=raw_data.get('logger_timestamp'),
                days_not_connection=raw_data.get('days_disconnected', 0),
                flow=processed_data.flow,
                pulses=processed_data.pulses,
                total=processed_data.total,
                total_diff=raw_data.get('total_diff', 0),
                total_today_diff=raw_data.get('total_today_diff', 0),
                level=processed_data.level,
                water_table=processed_data.level,
                send_dga=raw_data.get('send_dga', False),
                dga_response=raw_data.get('return_dga', ''),
                dga_voucher=raw_data.get('n_voucher', ''),
                is_error=not processed_data.is_valid
            )
            
            # Crear notificaciones si hay alertas
            if processed_data.alerts:
                for alert_message in processed_data.alerts:
                    NotificationsCatchment.objects.create(
                        point_catchment=catchment_point,
                        type_variable='telemetry',
                        type_notification='alert',
                        message=alert_message,
                        is_active=True
                    )
            
            # Enviar email de alerta si está habilitado
            if processed_data.alerts and self.config.processing_settings['alert_email_enabled']:
                self._send_alert_email(catchment_point, processed_data.alerts)
            
            return telemetry
    
    def _send_alert_email(self, catchment_point: CatchmentPoint, alerts: List[str]):
        """Enviar email de alerta al usuario del punto de captación"""
        try:
            if not catchment_point.user or not catchment_point.user.email:
                logger.warning(f"No hay email configurado para punto {catchment_point.id}")
                return
            
            subject = f"Alerta Telemetría - Punto {catchment_point.name}"
            message = f"""
            Se han detectado las siguientes alertas en el punto de captación {catchment_point.name}:
            
            {chr(10).join([f"- {alert}" for alert in alerts])}
            
            Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            Por favor, revise el estado del equipo.
            """
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[catchment_point.user.email],
                fail_silently=True
            )
            
            logger.info(f"Email de alerta enviado para punto {catchment_point.id}")
            
        except Exception as e:
            logger.error(f"Error enviando email de alerta para punto {catchment_point.id}: {str(e)}")


# Instancia global del procesador
telemetry_processor = TelemetryProcessor()
