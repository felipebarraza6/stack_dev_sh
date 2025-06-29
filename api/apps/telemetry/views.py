"""
Views para la API de telemetría
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count, Avg, Max, Min, Sum
from django.utils import timezone
from datetime import datetime, timedelta
import pytz

from .models.measurements import Measurement, MeasurementBatch, MeasurementQuality
from .models.points import CatchmentPoint
from .models.schemes import Variable, Scheme
from .serializers import (
    MeasurementSerializer, MeasurementBatchSerializer, MeasurementQualitySerializer,
    MeasurementQuerySerializer, MeasurementStatsSerializer, TimeSeriesSerializer,
    VariableSerializer, CatchmentPointSerializer, SchemeSerializer,
    BulkMeasurementSerializer, MeasurementExportSerializer
)

# Configuración de zona horaria
CHILE_TZ = pytz.timezone('America/Santiago')


class MeasurementViewSet(viewsets.ModelViewSet):
    """
    ViewSet para mediciones de telemetría
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['point__name', 'variable__name', 'provider']
    ordering_fields = ['timestamp', 'value_numeric', 'quality_score', 'created_at']
    ordering = ['-timestamp']

    def get_queryset(self):
        """Filtrar queryset según parámetros"""
        queryset = super().get_queryset()
        
        # Filtros básicos
        point_id = self.request.query_params.get('point_id')
        variable_id = self.request.query_params.get('variable_id')
        provider = self.request.query_params.get('provider')
        quality_min = self.request.query_params.get('quality_min')
        
        if point_id:
            queryset = queryset.filter(point_id=point_id)
        if variable_id:
            queryset = queryset.filter(variable_id=variable_id)
        if provider:
            queryset = queryset.filter(provider=provider)
        if quality_min:
            queryset = queryset.filter(quality_score__gte=float(quality_min))
        
        # Filtros de fecha
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        return queryset.select_related('point', 'variable')

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Crear múltiples mediciones"""
        serializer = BulkMeasurementSerializer(data=request.data)
        if serializer.is_valid():
            measurements_data = serializer.validated_data['measurements']
            
            # Crear mediciones
            measurements = []
            for measurement_data in measurements_data:
                measurement = Measurement(**measurement_data)
                measurements.append(measurement)
            
            # Bulk insert
            Measurement.objects.bulk_create(measurements)
            
            return Response({
                'message': f'{len(measurements)} mediciones creadas exitosamente',
                'count': len(measurements)
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Obtener estadísticas de mediciones"""
        now = timezone.now()
        today = now.date()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        # Estadísticas básicas
        total_measurements = Measurement.objects.count()
        measurements_today = Measurement.objects.filter(
            timestamp__date=today
        ).count()
        measurements_this_week = Measurement.objects.filter(
            timestamp__gte=week_ago
        ).count()
        measurements_this_month = Measurement.objects.filter(
            timestamp__gte=month_ago
        ).count()
        
        # Por proveedor
        by_provider = Measurement.objects.values('provider').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Por variable
        by_variable = Measurement.objects.values(
            'variable__name', 'variable__label'
        ).annotate(
            count=Count('id'),
            avg_quality=Avg('quality_score')
        ).order_by('-count')
        
        # Estadísticas de calidad
        quality_stats = Measurement.objects.aggregate(
            avg_quality=Avg('quality_score'),
            min_quality=Min('quality_score'),
            max_quality=Max('quality_score')
        )
        
        # Estadísticas de procesamiento
        processing_stats = MeasurementBatch.objects.aggregate(
            total_batches=Count('id'),
            completed_batches=Count('id', filter=Q(status='completed')),
            avg_processing_time=Avg('processing_time_ms')
        )
        
        stats = {
            'total_measurements': total_measurements,
            'measurements_today': measurements_today,
            'measurements_this_week': measurements_this_week,
            'measurements_this_month': measurements_this_month,
            'by_provider': {item['provider']: item['count'] for item in by_provider},
            'by_variable': {
                item['variable__name']: {
                    'count': item['count'],
                    'avg_quality': item['avg_quality']
                } for item in by_variable
            },
            'quality_stats': quality_stats,
            'processing_stats': processing_stats
        }
        
        return Response(stats)

    @action(detail=False, methods=['post'])
    def time_series(self, request):
        """Obtener serie temporal de mediciones"""
        serializer = TimeSeriesSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Construir queryset base
            queryset = Measurement.objects.filter(
                variable_id=data['variable_id'],
                timestamp__range=[data['start_date'], data['end_date']]
            )
            
            if data.get('point_id'):
                queryset = queryset.filter(point_id=data['point_id'])
            
            # Aplicar agregación según intervalo
            interval = data.get('interval', '1h')
            aggregation = data.get('aggregation', 'avg')
            
            # TODO: Implementar agregación por intervalos de tiempo
            # Por ahora retornamos datos sin agregar
            measurements = queryset.order_by('timestamp')
            
            serializer = MeasurementSerializer(measurements, many=True)
            return Response({
                'variable_id': data['variable_id'],
                'start_date': data['start_date'],
                'end_date': data['end_date'],
                'interval': interval,
                'aggregation': aggregation,
                'measurements': serializer.data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def export(self, request):
        """Exportar mediciones"""
        serializer = MeasurementExportSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Construir queryset
            queryset = Measurement.objects.all()
            
            if data.get('point_ids'):
                queryset = queryset.filter(point_id__in=data['point_ids'])
            if data.get('variable_ids'):
                queryset = queryset.filter(variable_id__in=data['variable_ids'])
            if data.get('start_date'):
                queryset = queryset.filter(timestamp__gte=data['start_date'])
            if data.get('end_date'):
                queryset = queryset.filter(timestamp__lte=data['end_date'])
            
            # Seleccionar campos según configuración
            fields = ['id', 'point__name', 'variable__name', 'timestamp', 
                     'value_numeric', 'value_text', 'value_boolean', 
                     'provider', 'quality_score']
            
            if data.get('include_raw_data'):
                fields.append('raw_value')
            if data.get('include_quality_metrics'):
                fields.append('quality_metrics')
            
            measurements = queryset.values(*fields)
            
            # TODO: Implementar exportación real según formato
            return Response({
                'message': 'Exportación iniciada',
                'format': data['format'],
                'count': len(measurements),
                'download_url': f'/api/telemetry/measurements/export/{data["format"]}/'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeasurementBatchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para lotes de mediciones (solo lectura)
    """
    queryset = MeasurementBatch.objects.all()
    serializer_class = MeasurementBatchSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-created_at']

    def get_queryset(self):
        """Filtrar por proveedor y estado"""
        queryset = super().get_queryset()
        
        provider = self.request.query_params.get('provider')
        status_filter = self.request.query_params.get('status')
        
        if provider:
            queryset = queryset.filter(provider=provider)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Estadísticas de lotes"""
        stats = MeasurementBatch.objects.aggregate(
            total_batches=Count('id'),
            completed_batches=Count('id', filter=Q(status='completed')),
            failed_batches=Count('id', filter=Q(status='failed')),
            avg_processing_time=Avg('processing_time_ms'),
            total_measurements=Sum('total_measurements'),
            processed_measurements=Sum('processed_measurements')
        )
        
        return Response(stats)


class MeasurementQualityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para métricas de calidad (solo lectura)
    """
    queryset = MeasurementQuality.objects.all()
    serializer_class = MeasurementQualitySerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-created_at']

    def get_queryset(self):
        """Filtrar por calidad"""
        queryset = super().get_queryset()
        
        is_outlier = self.request.query_params.get('is_outlier')
        is_missing = self.request.query_params.get('is_missing')
        
        if is_outlier is not None:
            queryset = queryset.filter(is_outlier=is_outlier)
        if is_missing is not None:
            queryset = queryset.filter(is_missing=is_missing)
        
        return queryset.select_related('measurement')


class VariableViewSet(viewsets.ModelViewSet):
    """
    ViewSet para variables de telemetría
    """
    queryset = Variable.objects.all()
    serializer_class = VariableSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'label', 'variable_type']
    ordering_fields = ['name', 'variable_type', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        """Filtrar por esquema y proveedor"""
        queryset = super().get_queryset()
        
        scheme_id = self.request.query_params.get('scheme_id')
        provider = self.request.query_params.get('provider')
        variable_type = self.request.query_params.get('variable_type')
        
        if scheme_id:
            queryset = queryset.filter(scheme_id=scheme_id)
        if provider:
            queryset = queryset.filter(provider=provider)
        if variable_type:
            queryset = queryset.filter(variable_type=variable_type)
        
        return queryset.select_related('scheme')

    @action(detail=True, methods=['get'])
    def measurements(self, request, pk=None):
        """Obtener mediciones de una variable específica"""
        variable = self.get_object()
        measurements = variable.measurements.all()
        
        # Aplicar filtros
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        limit = int(request.query_params.get('limit', 1000))
        
        if start_date:
            measurements = measurements.filter(timestamp__gte=start_date)
        if end_date:
            measurements = measurements.filter(timestamp__lte=end_date)
        
        measurements = measurements.order_by('-timestamp')[:limit]
        
        serializer = MeasurementSerializer(measurements, many=True)
        return Response(serializer.data)


class CatchmentPointViewSet(viewsets.ModelViewSet):
    """
    ViewSet para puntos de captación
    """
    queryset = CatchmentPoint.objects.all()
    serializer_class = CatchmentPointSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'project__name']
    ordering_fields = ['name', 'frequency', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        """Filtrar por proyecto y estado de telemetría"""
        queryset = super().get_queryset()
        
        project_id = self.request.query_params.get('project_id')
        is_telemetry_active = self.request.query_params.get('is_telemetry_active')
        frequency = self.request.query_params.get('frequency')
        
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if is_telemetry_active is not None:
            queryset = queryset.filter(is_telemetry_active=is_telemetry_active)
        if frequency:
            queryset = queryset.filter(frequency=frequency)
        
        return queryset.select_related('project', 'owner')

    @action(detail=True, methods=['get'])
    def measurements(self, request, pk=None):
        """Obtener mediciones de un punto específico"""
        point = self.get_object()
        measurements = point.measurements.all()
        
        # Aplicar filtros
        variable_id = request.query_params.get('variable_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        limit = int(request.query_params.get('limit', 1000))
        
        if variable_id:
            measurements = measurements.filter(variable_id=variable_id)
        if start_date:
            measurements = measurements.filter(timestamp__gte=start_date)
        if end_date:
            measurements = measurements.filter(timestamp__lte=end_date)
        
        measurements = measurements.order_by('-timestamp')[:limit]
        
        serializer = MeasurementSerializer(measurements, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def activate_telemetry(self, request, pk=None):
        """Activar telemetría para un punto"""
        point = self.get_object()
        point.is_telemetry_active = True
        point.telemetry_start_date = timezone.now().date()
        point.save()
        
        return Response({
            'message': f'Telemetría activada para {point.name}',
            'telemetry_start_date': point.telemetry_start_date
        })

    @action(detail=True, methods=['post'])
    def deactivate_telemetry(self, request, pk=None):
        """Desactivar telemetría para un punto"""
        point = self.get_object()
        point.is_telemetry_active = False
        point.save()
        
        return Response({
            'message': f'Telemetría desactivada para {point.name}'
        })


class SchemeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para esquemas de telemetría
    """
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['post'])
    def assign_to_points(self, request, pk=None):
        """Asignar esquema a puntos de captación"""
        scheme = self.get_object()
        point_ids = request.data.get('point_ids', [])
        
        if not point_ids:
            return Response(
                {'error': 'Se requieren point_ids'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        points = CatchmentPoint.objects.filter(id__in=point_ids)
        scheme.catchment_points.add(*points)
        
        return Response({
            'message': f'Esquema {scheme.name} asignado a {len(points)} puntos',
            'assigned_points': len(points)
        })

    @action(detail=True, methods=['post'])
    def remove_from_points(self, request, pk=None):
        """Remover esquema de puntos de captación"""
        scheme = self.get_object()
        point_ids = request.data.get('point_ids', [])
        
        if not point_ids:
            return Response(
                {'error': 'Se requieren point_ids'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        points = CatchmentPoint.objects.filter(id__in=point_ids)
        scheme.catchment_points.remove(*points)
        
        return Response({
            'message': f'Esquema {scheme.name} removido de {len(points)} puntos',
            'removed_points': len(points)
        }) 