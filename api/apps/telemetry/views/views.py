"""
Vistas Centralizadas de Telemetría
Endpoints optimizados para consultar datos de puntos de captación
"""
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from django.db.models import Q, Avg, Max, Min, Sum, Count
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone

from api.apps.catchment.models import CatchmentPoint
from api.apps.telemetry.models.models import TelemetryData
from api.apps.telemetry.serializers.serializers import (
    TelemetryDataSerializer,
    TelemetryDataCreateSerializer,
    TelemetryDataUpdateSerializer,
    TelemetryDataBulkCreateSerializer,
    TelemetryDataSummarySerializer,
    TelemetryDataChartSerializer,
    TelemetryDataExportSerializer,
    TelemetryDashboardSerializer,
    TelemetryMonthlySummarySerializer,
    TelemetryPointDetailsSerializer,
    TelemetryAlertsSerializer,
    TelemetrySystemStatusSerializer
)

logger = logging.getLogger(__name__)


class TelemetryPagination(PageNumberPagination):
    """Paginación personalizada para telemetría"""
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class TelemetryFilter(filters.FilterSet):
    """Filtros para consultas de telemetría"""
    class Meta:
        model = TelemetryData
        fields = {
            'catchment_point': ['exact', 'in'],
            'measurement_time': ['gte', 'lte', 'date', 'date__gte', 'date__lte'],
            'flow': ['gte', 'lte', 'exact'],
            'total': ['gte', 'lte', 'exact'],
            'water_table': ['gte', 'lte', 'exact'],
            'is_error': ['exact'],
            'send_dga': ['exact'],
        }


class TelemetryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vista centralizada para consultar datos de telemetría
    Optimizada para consultas eficientes con caché y filtros avanzados
    """
    permission_classes = [IsAuthenticated]
    pagination_class = TelemetryPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TelemetryFilter
    serializer_class = TelemetryDataSerializer
    
    def get_queryset(self):
        """Obtener queryset optimizado con select_related"""
        return TelemetryData.objects.select_related(
            'catchment_point', 
            'catchment_point__owner'
        ).order_by('-measurement_time')
    
    @method_decorator(cache_page(300))  # Cache por 5 minutos
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """
        Endpoint para dashboard con resumen de datos
        Incluye estadísticas generales y alertas
        """
        try:
            # Obtener parámetros de filtro
            catchment_point_id = request.query_params.get('catchment_point')
            date_from = request.query_params.get('date_from')
            date_to = request.query_params.get('date_to')
            
            # Construir filtros
            filters = Q()
            if catchment_point_id:
                filters &= Q(catchment_point_id=catchment_point_id)
            if date_from:
                filters &= Q(measurement_time__date__gte=date_from)
            if date_to:
                filters &= Q(measurement_time__date__lte=date_to)
            
            # Obtener datos base
            queryset = self.get_queryset().filter(filters)
            
            # Calcular estadísticas
            stats = queryset.aggregate(
                total_records=Count('id'),
                avg_flow=Avg('flow'),
                max_flow=Max('flow'),
                min_flow=Min('flow'),
                avg_level=Avg('water_table'),
                max_level=Max('water_table'),
                min_level=Min('water_table'),
                total_errors=Count('id', filter=Q(is_error=True)),
                total_dga_sent=Count('id', filter=Q(send_dga=True))
            )
            
            # Obtener últimos registros
            latest_records = queryset[:10]
            latest_serializer = self.get_serializer(latest_records, many=True)
            
            # Obtener puntos de captación activos
            active_points = CatchmentPoint.objects.filter(
                interactiondetail__isnull=False
            ).distinct().count()
            
            response_data = {
                'statistics': {
                    'total_records': stats['total_records'],
                    'active_points': active_points,
                    'flow': {
                        'average': float(stats['avg_flow'] or 0),
                        'maximum': float(stats['max_flow'] or 0),
                        'minimum': float(stats['min_flow'] or 0)
                    },
                    'level': {
                        'average': float(stats['avg_level'] or 0),
                        'maximum': float(stats['max_level'] or 0),
                        'minimum': float(stats['min_level'] or 0)
                    },
                    'errors': stats['total_errors'],
                    'dga_sent': stats['total_dga_sent']
                },
                'latest_records': latest_serializer.data,
                'filters_applied': {
                    'catchment_point': catchment_point_id,
                    'date_from': date_from,
                    'date_to': date_to
                }
            }
            
            return Response(response_data)
            
        except Exception as e:
            logger.error(f"Error en dashboard: {str(e)}")
            return Response(
                {'error': 'Error interno del servidor'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @method_decorator(cache_page(600))  # Cache por 10 minutos
    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        """
        Endpoint para resumen mensual por punto de captación
        Agrupa datos por mes y punto de captación
        """
        try:
            # Obtener parámetros
            year = request.query_params.get('year', datetime.now().year)
            month = request.query_params.get('month', datetime.now().month)
            catchment_point_id = request.query_params.get('catchment_point')
            
            # Construir filtros
            filters = Q(
                date_time_medition__year=year,
                date_time_medition__month=month
            )
            if catchment_point_id:
                filters &= Q(catchment_point_id=catchment_point_id)
            
            # Obtener datos del mes
            monthly_data = self.get_queryset().filter(filters)
            
            # Agrupar por punto de captación
            points_summary = []
            points = monthly_data.values('catchment_point').distinct()
            
            for point in points:
                point_id = point['catchment_point']
                point_data = monthly_data.filter(catchment_point_id=point_id)
                
                # Calcular estadísticas del punto
                point_stats = point_data.aggregate(
                    total_records=Count('id'),
                    avg_flow=Avg('flow'),
                    max_flow=Max('flow'),
                    min_flow=Min('flow'),
                    avg_level=Avg('water_table'),
                    max_level=Max('water_table'),
                    min_level=Min('water_table'),
                    total_errors=Count('id', filter=Q(is_error=True)),
                    total_dga_sent=Count('id', filter=Q(send_dga=True))
                )
                
                # Obtener información del punto
                catchment_point = CatchmentPoint.objects.get(id=point_id)
                
                points_summary.append({
                    'catchment_point': {
                        'id': point_id,
                        'name': catchment_point.name,
                        'location': catchment_point.location_display
                    },
                    'statistics': {
                        'total_records': point_stats['total_records'],
                        'flow': {
                            'average': float(point_stats['avg_flow'] or 0),
                            'maximum': float(point_stats['max_flow'] or 0),
                            'minimum': float(point_stats['min_flow'] or 0)
                        },
                        'level': {
                            'average': float(point_stats['avg_level'] or 0),
                            'maximum': float(point_stats['max_level'] or 0),
                            'minimum': float(point_stats['min_level'] or 0)
                        },
                        'errors': point_stats['total_errors'],
                        'dga_sent': point_stats['total_dga_sent']
                    }
                })
            
            response_data = {
                'period': {
                    'year': int(year),
                    'month': int(month)
                },
                'points_summary': points_summary,
                'total_points': len(points_summary)
            }
            
            return Response(response_data)
            
        except Exception as e:
            logger.error(f"Error en monthly_summary: {str(e)}")
            return Response(
                {'error': 'Error interno del servidor'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @method_decorator(cache_page(1800))  # Cache por 30 minutos
    @action(detail=False, methods=['get'])
    def point_details(self, request):
        """
        Endpoint para detalles específicos de un punto de captación
        Incluye historial y tendencias
        """
        try:
            catchment_point_id = request.query_params.get('catchment_point')
            if not catchment_point_id:
                return Response(
                    {'error': 'Se requiere catchment_point'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Obtener parámetros de tiempo
            days = int(request.query_params.get('days', 30))
            date_from = datetime.now() - timedelta(days=days)
            
            # Obtener datos del punto
            point_data = self.get_queryset().filter(
                catchment_point_id=catchment_point_id,
                date_time_medition__gte=date_from
            )
            
            if not point_data.exists():
                return Response(
                    {'error': 'No se encontraron datos para este punto'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Calcular estadísticas detalladas
            stats = point_data.aggregate(
                total_records=Count('id'),
                avg_flow=Avg('flow'),
                max_flow=Max('flow'),
                min_flow=Min('flow'),
                avg_level=Avg('water_table'),
                max_level=Max('water_table'),
                min_level=Min('water_table'),
                total_errors=Count('id', filter=Q(is_error=True)),
                total_dga_sent=Count('id', filter=Q(send_dga=True))
            )
            
            # Obtener tendencias diarias
            daily_trends = point_data.extra(
                select={'day': 'date(date_time_medition)'}
            ).values('day').annotate(
                avg_flow=Avg('flow'),
                avg_level=Avg('water_table'),
                record_count=Count('id')
            ).order_by('day')
            
            # Obtener información del punto
            catchment_point = CatchmentPoint.objects.get(id=catchment_point_id)
            
            response_data = {
                'catchment_point': {
                    'id': catchment_point_id,
                    'name': catchment_point.name,
                    'location': catchment_point.location_display,
                    'code': catchment_point.code
                },
                'statistics': {
                    'total_records': stats['total_records'],
                    'flow': {
                        'average': float(stats['avg_flow'] or 0),
                        'maximum': float(stats['max_flow'] or 0),
                        'minimum': float(stats['min_flow'] or 0)
                    },
                    'level': {
                        'average': float(stats['avg_level'] or 0),
                        'maximum': float(stats['max_level'] or 0),
                        'minimum': float(stats['min_level'] or 0)
                    },
                    'errors': stats['total_errors'],
                    'dga_sent': stats['total_dga_sent']
                },
                'daily_trends': list(daily_trends),
                'period': {
                    'days': days,
                    'date_from': date_from.isoformat(),
                    'date_to': datetime.now().isoformat()
                }
            }
            
            return Response(response_data)
            
        except Exception as e:
            logger.error(f"Error en point_details: {str(e)}")
            return Response(
                {'error': 'Error interno del servidor'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def alerts(self, request):
        """
        Endpoint para obtener alertas y errores
        Filtra registros con errores o valores anómalos
        """
        try:
            # Obtener parámetros
            days = int(request.query_params.get('days', 7))
            date_from = datetime.now() - timedelta(days=days)
            
            # Obtener registros con errores o valores anómalos
            alerts_data = self.get_queryset().filter(
                Q(is_error=True) | 
                Q(flow=0) |  # Caudal en 0
                Q(water_table__gte=90)  # Nivel crítico
            ).filter(
                date_time_medition__gte=date_from
            )
            
            # Serializar datos
            serializer = self.get_serializer(alerts_data, many=True)
            
            response_data = {
                'alerts': serializer.data,
                'total_alerts': alerts_data.count(),
                'period': {
                    'days': days,
                    'date_from': date_from.isoformat(),
                    'date_to': datetime.now().isoformat()
                }
            }
            
            return Response(response_data)
            
        except Exception as e:
            logger.error(f"Error en alerts: {str(e)}")
            return Response(
                {'error': 'Error interno del servidor'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @method_decorator(cache_page(3600))  # Cache por 1 hora
    @action(detail=False, methods=['get'])
    def system_status(self, request):
        """
        Endpoint para estado general del sistema
        Incluye información de configuración y salud del sistema
        """
        try:
            # Obtener estadísticas generales
            total_points = CatchmentPoint.objects.count()
            active_points = CatchmentPoint.objects.filter(
                interactiondetail__isnull=False
            ).distinct().count()
            
            # Obtener configuración del sistema
            config_info = {
                'variables': ['flow', 'total', 'level', 'water_table'],
                'providers': ['Twin', 'Nettra', 'Novus'],
                'processing_settings': {
                    'sampling_frequency': 60,
                    'cache_duration': 300
                }
            }
            
            # Obtener últimos registros del sistema
            latest_records = self.get_queryset()[:5]
            latest_serializer = self.get_serializer(latest_records, many=True)
            
            response_data = {
                'system_info': {
                    'total_points': total_points,
                    'active_points': active_points,
                    'last_update': datetime.now().isoformat()
                },
                'configuration': config_info,
                'latest_activity': latest_serializer.data
            }
            
            return Response(response_data)
            
        except Exception as e:
            logger.error(f"Error en system_status: {str(e)}")
            return Response(
                {'error': 'Error interno del servidor'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 