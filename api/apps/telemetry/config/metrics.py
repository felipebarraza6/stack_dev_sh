"""
Sistema de Métricas para Prometheus
Expone métricas del sistema de telemetría para monitoreo
"""
import logging
from typing import Dict, Any
from datetime import datetime, timedelta
from django.db.models import Count, Avg, Max, Min, Q
from django.core.cache import cache
from prometheus_client import Counter, Gauge, Histogram, Summary, generate_latest, CONTENT_TYPE_LATEST
from django.http import HttpResponse

from api.apps.catchment.models import CatchmentPoint, NotificationsCatchment
from .models import TelemetryData
from api.telemetry.config import telemetry_config

logger = logging.getLogger(__name__)


class TelemetryMetrics:
    """Gestor de métricas para el sistema de telemetría"""
    
    def __init__(self):
        self._initialize_metrics()
    
    def _initialize_metrics(self):
        """Inicializar todas las métricas de Prometheus"""
        
        # Métricas de caudal
        self.flow_gauge = Gauge(
            'telemetry_flow_litros_segundo',
            'Caudal actual en litros por segundo',
            ['catchment_point', 'device_id']
        )
        
        self.flow_avg = Gauge(
            'telemetry_flow_promedio',
            'Caudal promedio en los últimos 5 minutos',
            ['catchment_point']
        )
        
        # Métricas de nivel
        self.level_gauge = Gauge(
            'telemetry_level_metros',
            'Nivel freático actual en metros',
            ['catchment_point', 'device_id']
        )
        
        self.level_avg = Gauge(
            'telemetry_level_promedio',
            'Nivel promedio en los últimos 5 minutos',
            ['catchment_point']
        )
        
        # Métricas de totalizado
        self.total_gauge = Gauge(
            'telemetry_total_metros_cubicos',
            'Total acumulado en metros cúbicos',
            ['catchment_point', 'device_id']
        )
        
        self.total_inconsistency = Gauge(
            'telemetry_total_inconsistencia',
            'Indicador de inconsistencia en totalizado (1=inconsistente, 0=consistente)',
            ['catchment_point']
        )
        
        # Métricas de tiempo
        self.last_measurement = Gauge(
            'telemetry_ultima_medicion',
            'Timestamp de la última medición',
            ['catchment_point']
        )
        
        # Métricas de errores
        self.error_counter = Counter(
            'telemetry_errores_total',
            'Total de errores por punto de captación',
            ['catchment_point', 'error_type']
        )
        
        # Métricas de proveedores
        self.provider_errors = Counter(
            'telemetry_proveedor_errores',
            'Errores por proveedor',
            ['proveedor', 'error_type']
        )
        
        self.provider_success = Counter(
            'telemetry_proveedor_exitos',
            'Éxitos por proveedor',
            ['proveedor']
        )
        
        # Métricas de DGA
        self.dga_queue_size = Gauge(
            'telemetry_dga_cola_elementos',
            'Número de elementos en cola DGA'
        )
        
        self.dga_sent = Counter(
            'telemetry_dga_enviados_total',
            'Total de registros enviados a DGA',
            ['catchment_point', 'status']
        )
        
        self.dga_errors = Counter(
            'telemetry_dga_errores_envio',
            'Errores de envío a DGA',
            ['error_type']
        )
        
        # Métricas de API
        self.api_requests = Counter(
            'telemetry_api_requests_total',
            'Total de peticiones a la API',
            ['endpoint', 'method', 'status']
        )
        
        self.api_duration = Histogram(
            'telemetry_api_request_duration_seconds',
            'Duración de peticiones a la API',
            ['endpoint', 'method']
        )
        
        # Métricas de sistema
        self.active_points = Gauge(
            'telemetry_puntos_activos',
            'Número de puntos de captación activos'
        )
        
        self.total_records = Gauge(
            'telemetry_registros_total',
            'Total de registros en la base de datos'
        )
        
        self.alerts_active = Gauge(
            'telemetry_alertas_activas',
            'Número de alertas activas',
            ['alert_type']
        )
    
    def update_flow_metrics(self, catchment_point: CatchmentPoint, flow: float):
        """Actualizar métricas de caudal"""
        try:
            self.flow_gauge.labels(
                catchment_point=str(catchment_point.id),
                device_id=catchment_point.device_id or 'unknown'
            ).set(flow)
            
            # Calcular promedio de los últimos 5 minutos
            five_minutes_ago = datetime.now() - timedelta(minutes=5)
            avg_flow = TelemetryData.objects.filter(
                catchment_point=catchment_point,
                measurement_time__gte=five_minutes_ago
            ).aggregate(avg=Avg('flow'))['avg'] or 0.0
            
            self.flow_avg.labels(
                catchment_point=str(catchment_point.id)
            ).set(avg_flow)
            
        except Exception as e:
            logger.error(f"Error actualizando métricas de caudal: {str(e)}")
    
    def update_level_metrics(self, catchment_point: CatchmentPoint, level: float):
        """Actualizar métricas de nivel"""
        try:
            self.level_gauge.labels(
                catchment_point=str(catchment_point.id),
                device_id=catchment_point.device_id or 'unknown'
            ).set(level)
            
            # Calcular promedio de los últimos 5 minutos
            five_minutes_ago = datetime.now() - timedelta(minutes=5)
            avg_level = TelemetryData.objects.filter(
                catchment_point=catchment_point,
                measurement_time__gte=five_minutes_ago
            ).aggregate(avg=Avg('water_table'))['avg'] or 0.0
            
            self.level_avg.labels(
                catchment_point=str(catchment_point.id)
            ).set(avg_level)
            
        except Exception as e:
            logger.error(f"Error actualizando métricas de nivel: {str(e)}")
    
    def update_total_metrics(self, catchment_point: CatchmentPoint, total: float, is_inconsistent: bool = False):
        """Actualizar métricas de totalizado"""
        try:
            self.total_gauge.labels(
                catchment_point=str(catchment_point.id),
                device_id=catchment_point.device_id or 'unknown'
            ).set(total)
            
            # Marcar inconsistencia si existe
            self.total_inconsistency.labels(
                catchment_point=str(catchment_point.id)
            ).set(1 if is_inconsistent else 0)
            
        except Exception as e:
            logger.error(f"Error actualizando métricas de total: {str(e)}")
    
    def update_last_measurement(self, catchment_point: CatchmentPoint):
        """Actualizar timestamp de última medición"""
        try:
            self.last_measurement.labels(
                catchment_point=str(catchment_point.id)
            ).set(datetime.now().timestamp())
            
        except Exception as e:
            logger.error(f"Error actualizando última medición: {str(e)}")
    
    def record_error(self, catchment_point: CatchmentPoint, error_type: str):
        """Registrar error"""
        try:
            self.error_counter.labels(
                catchment_point=str(catchment_point.id),
                error_type=error_type
            ).inc()
            
        except Exception as e:
            logger.error(f"Error registrando error: {str(e)}")
    
    def record_provider_error(self, provider: str, error_type: str):
        """Registrar error de proveedor"""
        try:
            self.provider_errors.labels(
                proveedor=provider,
                error_type=error_type
            ).inc()
            
        except Exception as e:
            logger.error(f"Error registrando error de proveedor: {str(e)}")
    
    def record_provider_success(self, provider: str):
        """Registrar éxito de proveedor"""
        try:
            self.provider_success.labels(
                proveedor=provider
            ).inc()
            
        except Exception as e:
            logger.error(f"Error registrando éxito de proveedor: {str(e)}")
    
    def update_dga_queue_size(self, size: int):
        """Actualizar tamaño de cola DGA"""
        try:
            self.dga_queue_size.set(size)
        except Exception as e:
            logger.error(f"Error actualizando tamaño de cola DGA: {str(e)}")
    
    def record_dga_sent(self, catchment_point: CatchmentPoint, status: str):
        """Registrar envío a DGA"""
        try:
            self.dga_sent.labels(
                catchment_point=str(catchment_point.id),
                status=status
            ).inc()
            
        except Exception as e:
            logger.error(f"Error registrando envío DGA: {str(e)}")
    
    def record_dga_error(self, error_type: str):
        """Registrar error de DGA"""
        try:
            self.dga_errors.labels(
                error_type=error_type
            ).inc()
            
        except Exception as e:
            logger.error(f"Error registrando error DGA: {str(e)}")
    
    def record_api_request(self, endpoint: str, method: str, status: int, duration: float):
        """Registrar petición a la API"""
        try:
            self.api_requests.labels(
                endpoint=endpoint,
                method=method,
                status=str(status)
            ).inc()
            
            self.api_duration.labels(
                endpoint=endpoint,
                method=method
            ).observe(duration)
            
        except Exception as e:
            logger.error(f"Error registrando petición API: {str(e)}")
    
    def update_system_metrics(self):
        """Actualizar métricas del sistema"""
        try:
            # Puntos activos (con datos en las últimas 24 horas)
            yesterday = datetime.now() - timedelta(days=1)
            active_count = CatchmentPoint.objects.filter(
                telemetry_data__measurement_time__gte=yesterday
            ).distinct().count()
            
            self.active_points.set(active_count)
            
            # Total de registros
            total_count = TelemetryData.objects.count()
            self.total_records.set(total_count)
            
            # Alertas activas
            active_alerts = NotificationsCatchment.objects.filter(
                is_active=True
            ).count()
            
            self.alerts_active.labels(
                alert_type='general'
            ).set(active_alerts)
            
        except Exception as e:
            logger.error(f"Error actualizando métricas del sistema: {str(e)}")


# Instancia global de métricas
telemetry_metrics = TelemetryMetrics()


def metrics_view(request):
    """Vista para exponer métricas de Prometheus"""
    try:
        # Actualizar métricas del sistema
        telemetry_metrics.update_system_metrics()
        
        # Generar respuesta de Prometheus
        response = HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)
        return response
        
    except Exception as e:
        logger.error(f"Error generando métricas: {str(e)}")
        return HttpResponse("Error generando métricas", status=500)


class MetricsMiddleware:
    """Middleware para registrar métricas de peticiones HTTP"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = datetime.now()
        
        response = self.get_response(request)
        
        # Calcular duración
        duration = (datetime.now() - start_time).total_seconds()
        
        # Registrar métrica
        telemetry_metrics.record_api_request(
            endpoint=request.path,
            method=request.method,
            status=response.status_code,
            duration=duration
        )
        
        return response 