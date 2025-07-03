"""
ViewSets Base para API Interna
Proporciona ViewSets base sin lógica de frontend
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from api.apps.core.api.base.serializers.base_serializers import (
    BaseViewSetSerializer,
    VariableBaseSerializer,
    VariableSchemaBaseSerializer,
    CatchmentPointBaseSerializer,
    TelemetryDataBaseSerializer
)


class BaseModelViewSet(viewsets.ModelViewSet):
    """ViewSet base para modelos que heredan de BaseModel"""
    
    serializer_class = BaseViewSetSerializer
    filter_backends = [filters.DjangoFilterBackend]
    
    def get_queryset(self):
        """Queryset base que filtra por is_active=True"""
        return self.queryset.filter(is_active=True)
    
    def perform_destroy(self, instance):
        """Soft delete en lugar de borrar físicamente"""
        instance.is_active = False
        instance.save()
    
    @action(detail=False, methods=['get'])
    def active_count(self, request):
        """Contar registros activos"""
        count = self.get_queryset().count()
        return Response({'count': count})


@extend_schema_view(
    list=extend_schema(
        summary="Listar variables",
        description="Obtener lista de variables del sistema",
        tags=["API Base", "Variables"],
        examples=[
            OpenApiExample(
                "Variables de nivel",
                value={
                    "count": 2,
                    "results": [
                        {
                            "id": 1,
                            "name": "Nivel de Agua",
                            "code": "NIVEL_001",
                            "variable_type": "NIVEL",
                            "unit": "METERS",
                            "is_active": True
                        }
                    ]
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Crear variable",
        description="Crear una nueva variable en el sistema",
        tags=["API Base", "Variables"],
        examples=[
            OpenApiExample(
                "Crear variable de nivel",
                value={
                    "name": "Nivel de Agua",
                    "code": "NIVEL_001",
                    "variable_type": "NIVEL",
                    "unit": "METERS"
                }
            )
        ]
    )
)
class VariableBaseViewSet(BaseModelViewSet):
    """ViewSet base para variables (API interna)"""
    
    from api.apps.variables.models.variables.variable import Variable
    queryset = Variable.objects.all()
    serializer_class = VariableBaseSerializer
    filterset_fields = ['variable_type', 'unit', 'is_active']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """Queryset optimizado para API interna"""
        queryset = super().get_queryset()
        
        # Filtros específicos
        variable_type = self.request.query_params.get('variable_type')
        if variable_type:
            queryset = queryset.filter(variable_type=variable_type)
        
        return queryset


class VariableSchemaBaseViewSet(BaseModelViewSet):
    """ViewSet base para esquemas de variables"""
    
    from api.apps.variables.models.schemas.schema import VariableSchema
    queryset = VariableSchema.objects.all()
    serializer_class = VariableSchemaBaseSerializer
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class CatchmentPointBaseViewSet(BaseModelViewSet):
    """ViewSet base para puntos de captación"""
    
    from api.apps.catchment.models.points.catchment_point import CatchmentPoint
    queryset = CatchmentPoint.objects.all()
    serializer_class = CatchmentPointBaseSerializer
    filterset_fields = ['point_type', 'provider', 'status', 'is_active']
    search_fields = ['name', 'code', 'device_id']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """Queryset optimizado para API interna"""
        queryset = super().get_queryset()
        
        # Filtros específicos
        point_type = self.request.query_params.get('point_type')
        if point_type:
            queryset = queryset.filter(point_type=point_type)
        
        provider = self.request.query_params.get('provider')
        if provider:
            queryset = queryset.filter(provider=provider)
        
        return queryset


class TelemetryDataBaseViewSet(BaseModelViewSet):
    """ViewSet base para datos de telemetría"""
    
    from api.apps.telemetry.models.data.telemetry_data import TelemetryData
    queryset = TelemetryData.objects.all()
    serializer_class = TelemetryDataBaseSerializer
    filterset_fields = ['catchment_point', 'is_warning', 'is_error', 'send_dga']
    ordering_fields = ['measurement_time', 'created_at']
    ordering = ['-measurement_time']
    
    def get_queryset(self):
        """Queryset optimizado para API interna"""
        queryset = super().get_queryset()
        
        # Filtros específicos
        catchment_point_id = self.request.query_params.get('catchment_point_id')
        if catchment_point_id:
            queryset = queryset.filter(catchment_point_id=catchment_point_id)
        
        # Filtro por fecha
        from_date = self.request.query_params.get('from_date')
        if from_date:
            queryset = queryset.filter(measurement_time__gte=from_date)
        
        to_date = self.request.query_params.get('to_date')
        if to_date:
            queryset = queryset.filter(measurement_time__lte=to_date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def latest_by_point(self, request):
        """Obtener último dato por punto de captación"""
        from django.db.models import Max
        
        latest_data = self.get_queryset().values('catchment_point').annotate(
            latest_time=Max('measurement_time')
        )
        
        return Response(latest_data) 