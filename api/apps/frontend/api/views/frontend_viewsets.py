"""
ViewSets Frontend para API Externa
Proporciona ViewSets optimizados para frontend con caché
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.cache import cache
from django.db.models import Count, Max, Min, Avg
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from api.apps.core.api.base.views.base_viewsets import (
    VariableBaseViewSet,
    VariableSchemaBaseViewSet,
    CatchmentPointBaseViewSet,
    TelemetryDataBaseViewSet
)
from ..serializers.frontend_serializers import (
    VariableFrontendSerializer,
    VariableSchemaFrontendSerializer,
    CatchmentPointFrontendSerializer,
    TelemetryDataFrontendSerializer
)


@extend_schema_view(
    list=extend_schema(
        summary="Listar variables para frontend",
        description="Obtener lista de variables con campos adicionales para frontend",
        tags=["API Frontend", "Variables"],
        examples=[
            OpenApiExample(
                "Variables con campos adicionales",
                value={
                    "count": 2,
                    "results": [
                        {
                            "id": 1,
                            "name": "Nivel de Agua",
                            "code": "NIVEL_001",
                            "display_name": "Nivel de Agua del Pozo",
                            "unit_display": "metros",
                            "status_display": "Activa",
                            "variable_type_display": "Nivel",
                            "is_active": True
                        }
                    ]
                }
            )
        ]
    ),
    dashboard_summary=extend_schema(
        summary="Dashboard de variables",
        description="Obtener resumen de variables para dashboard con caché",
        tags=["API Frontend", "Dashboard"],
        examples=[
            OpenApiExample(
                "Resumen de dashboard",
                value={
                    "total_variables": 25,
                    "active_variables": 23,
                    "variables_by_type": [
                        {"variable_type": "NIVEL", "count": 10},
                        {"variable_type": "CAUDAL", "count": 8}
                    ],
                    "recent_variables": [
                        {
                            "id": 1,
                            "name": "Nivel de Agua",
                            "created_at": "2024-01-15T10:30:00Z"
                        }
                    ]
                }
            )
        ]
    )
)
class VariableFrontendViewSet(VariableBaseViewSet):
    """ViewSet para frontend con caché y optimizaciones"""
    
    serializer_class = VariableFrontendSerializer
    
    def get_queryset(self):
        """Queryset optimizado para frontend"""
        queryset = super().get_queryset()
        
        # Optimizaciones específicas para frontend
        queryset = queryset.select_related()
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def dashboard_summary(self, request):
        """Endpoint específico para dashboard"""
        cache_key = f"variables_dashboard_summary_{request.user.id if request.user.is_authenticated else 'anonymous'}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        # Lógica específica para dashboard
        queryset = self.get_queryset()
        
        data = {
            'total_variables': queryset.count(),
            'active_variables': queryset.filter(is_active=True).count(),
            'variables_by_type': self.get_variables_by_type(),
            'recent_variables': self.get_recent_variables(),
        }
        
        # Cache por 5 minutos
        cache.set(cache_key, data, 300)
        
        return Response(data)
    
    def get_variables_by_type(self):
        """Obtener variables agrupadas por tipo"""
        return self.get_queryset().values('variable_type').annotate(
            count=Count('id')
        ).order_by('-count')
    
    def get_recent_variables(self):
        """Obtener variables recientes"""
        return self.get_queryset().filter(
            is_active=True
        ).order_by('-created_at')[:5]


class VariableSchemaFrontendViewSet(VariableSchemaBaseViewSet):
    """ViewSet para esquemas en frontend"""
    
    serializer_class = VariableSchemaFrontendSerializer
    
    @action(detail=True, methods=['post'])
    def assign_to_catchment_point(self, request, pk=None):
        """Asignar esquema a punto de captación"""
        schema = self.get_object()
        catchment_point_id = request.data.get('catchment_point_id')
        custom_config = request.data.get('custom_config', {})
        custom_labels = request.data.get('custom_labels', {})
        
        # Aquí implementarías la lógica para asignar el esquema
        # Por ahora retornamos un mensaje de éxito
        
        return Response({
            'status': 'assigned',
            'schema_id': schema.id,
            'catchment_point_id': catchment_point_id,
            'message': f'Esquema {schema.name} asignado al punto de captación'
        })
    
    @action(detail=False, methods=['get'])
    def available_for_assignment(self, request):
        """Obtener esquemas disponibles para asignación"""
        cache_key = "available_schemas_for_assignment"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        schemas = self.get_queryset().filter(is_active=True)
        data = self.get_serializer(schemas, many=True).data
        
        # Cache por 10 minutos
        cache.set(cache_key, data, 600)
        
        return Response(data)


class CatchmentPointFrontendViewSet(CatchmentPointBaseViewSet):
    """ViewSet para puntos de captación en frontend"""
    
    serializer_class = CatchmentPointFrontendSerializer
    
    def get_queryset(self):
        """Queryset optimizado para frontend"""
        queryset = super().get_queryset()
        
        # Optimizaciones específicas para frontend
        queryset = queryset.select_related('owner')
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def map_data(self, request):
        """Obtener datos para mapa"""
        cache_key = "catchment_points_map_data"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        points = self.get_queryset().filter(
            latitude__isnull=False,
            longitude__isnull=False
        ).values('id', 'name', 'latitude', 'longitude', 'status', 'point_type')
        
        data = list(points)
        
        # Cache por 15 minutos
        cache.set(cache_key, data, 900)
        
        return Response(data)
    
    @action(detail=True, methods=['get'])
    def variables(self, request, pk=None):
        """Obtener variables configuradas para un punto"""
        point = self.get_object()
        
        # Aquí implementarías la lógica para obtener variables del punto
        # Por ahora retornamos datos de ejemplo
        
        return Response({
            'point_id': point.id,
            'point_name': point.name,
            'variables': [],
            'message': 'Variables del punto de captación'
        })


class TelemetryDataFrontendViewSet(TelemetryDataBaseViewSet):
    """ViewSet para datos de telemetría en frontend"""
    
    serializer_class = TelemetryDataFrontendSerializer
    
    def get_queryset(self):
        """Queryset optimizado para frontend"""
        queryset = super().get_queryset()
        
        # Optimizaciones específicas para frontend
        queryset = queryset.select_related('catchment_point')
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def latest_summary(self, request):
        """Obtener resumen de últimos datos"""
        cache_key = "telemetry_latest_summary"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        queryset = self.get_queryset()
        
        data = {
            'total_records': queryset.count(),
            'latest_measurement': queryset.aggregate(
                latest=Max('measurement_time')
            )['latest'],
            'points_with_data': queryset.values('catchment_point').distinct().count(),
            'alerts_count': queryset.filter(is_warning=True).count(),
            'errors_count': queryset.filter(is_error=True).count(),
        }
        
        # Cache por 2 minutos
        cache.set(cache_key, data, 120)
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def chart_data(self, request):
        """Obtener datos para gráficos"""
        catchment_point_id = request.query_params.get('catchment_point_id')
        variable_type = request.query_params.get('variable_type')
        hours = int(request.query_params.get('hours', 24))
        
        cache_key = f"telemetry_chart_data_{catchment_point_id}_{variable_type}_{hours}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        from django.utils import timezone
        from datetime import timedelta
        
        queryset = self.get_queryset()
        
        if catchment_point_id:
            queryset = queryset.filter(catchment_point_id=catchment_point_id)
        
        # Filtrar por las últimas N horas
        since = timezone.now() - timedelta(hours=hours)
        queryset = queryset.filter(measurement_time__gte=since)
        
        # Agrupar por hora y obtener promedios
        data = queryset.extra(
            select={'hour': "date_trunc('hour', measurement_time)"}
        ).values('hour').annotate(
            avg_level=Avg('level'),
            avg_flow=Avg('flow'),
            avg_temperature=Avg('temperature'),
            count=Count('id')
        ).order_by('hour')
        
        # Cache por 5 minutos
        cache.set(cache_key, list(data), 300)
        
        return Response(data) 