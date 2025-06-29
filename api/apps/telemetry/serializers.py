"""
Serializers para la API de telemetría
"""
from rest_framework import serializers
from django.db.models import Avg, Max, Min, Count
from datetime import datetime, timedelta
import pytz

from .models.measurements import Measurement, MeasurementBatch, MeasurementQuality
from .models.points import CatchmentPoint
from .models.schemes import Variable, Scheme

# Configuración de zona horaria
CHILE_TZ = pytz.timezone('America/Santiago')

class MeasurementSerializer(serializers.ModelSerializer):
    """Serializer para mediciones individuales"""
    point_name = serializers.CharField(source='point.name', read_only=True)
    variable_name = serializers.CharField(source='variable.name', read_only=True)
    variable_label = serializers.CharField(source='variable.label', read_only=True)
    variable_unit = serializers.CharField(source='variable.unit', read_only=True)
    
    class Meta:
        model = Measurement
        fields = [
            'id', 'point', 'point_name', 'variable', 'variable_name', 
            'variable_label', 'variable_unit', 'timestamp', 'value_numeric',
            'value_text', 'value_boolean', 'raw_value', 'quality_score',
            'provider', 'processing_config', 'days_since_last_connection',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class MeasurementQualitySerializer(serializers.ModelSerializer):
    """Serializer para métricas de calidad"""
    
    class Meta:
        model = MeasurementQuality
        fields = [
            'id', 'measurement', 'outlier_score', 'consistency_score',
            'completeness_score', 'is_outlier', 'is_missing', 'is_interpolated',
            'quality_notes', 'overall_quality_score', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'overall_quality_score', 'created_at', 'updated_at']

class MeasurementBatchSerializer(serializers.ModelSerializer):
    """Serializer para lotes de mediciones"""
    success_rate = serializers.FloatField(read_only=True)
    
    class Meta:
        model = MeasurementBatch
        fields = [
            'id', 'batch_id', 'provider', 'frequency', 'total_measurements',
            'processed_measurements', 'failed_measurements', 'processing_time_ms',
            'status', 'metadata', 'success_rate', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'success_rate', 'created_at', 'updated_at']

class MeasurementStatsSerializer(serializers.Serializer):
    """Serializer para estadísticas de mediciones"""
    total_measurements = serializers.IntegerField()
    measurements_today = serializers.IntegerField()
    measurements_this_week = serializers.IntegerField()
    measurements_this_month = serializers.IntegerField()
    by_provider = serializers.DictField()
    by_variable = serializers.DictField()
    quality_stats = serializers.DictField()
    processing_stats = serializers.DictField()

class MeasurementQuerySerializer(serializers.Serializer):
    """Serializer para consultas de mediciones"""
    point_id = serializers.IntegerField(required=False)
    variable_id = serializers.IntegerField(required=False)
    provider = serializers.CharField(required=False)
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)
    frequency = serializers.CharField(required=False)
    quality_min = serializers.FloatField(required=False, min_value=0.0, max_value=1.0)
    limit = serializers.IntegerField(required=False, min_value=1, max_value=10000, default=1000)
    offset = serializers.IntegerField(required=False, min_value=0, default=0)
    
    def validate(self, data):
        """Validar fechas"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("start_date debe ser anterior a end_date")
        
        return data

class TimeSeriesSerializer(serializers.Serializer):
    """Serializer para series temporales"""
    variable_id = serializers.IntegerField()
    point_id = serializers.IntegerField(required=False)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    interval = serializers.CharField(required=False, default='1h')  # 1h, 1d, 1w, 1m
    aggregation = serializers.CharField(required=False, default='avg')  # avg, min, max, sum, count
    
    def validate(self, data):
        """Validar parámetros de serie temporal"""
        start_date = data['start_date']
        end_date = data['end_date']
        
        if start_date >= end_date:
            raise serializers.ValidationError("start_date debe ser anterior a end_date")
        
        # Validar que el rango no sea muy grande
        time_diff = end_date - start_date
        if time_diff > timedelta(days=365):
            raise serializers.ValidationError("El rango máximo es de 1 año")
        
        return data

class VariableSerializer(serializers.ModelSerializer):
    """Serializer para variables"""
    scheme_name = serializers.CharField(source='scheme.name', read_only=True)
    measurements_count = serializers.SerializerMethodField()
    last_measurement = serializers.SerializerMethodField()
    
    class Meta:
        model = Variable
        fields = [
            'id', 'scheme', 'scheme_name', 'name', 'label', 'variable_type',
            'provider', 'unit', 'pulse_factor', 'constant_addition',
            'extra_attributes', 'measurements_count', 'last_measurement',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'measurements_count', 'last_measurement', 'created_at', 'updated_at']
    
    def get_measurements_count(self, obj):
        """Obtener conteo de mediciones para esta variable"""
        return obj.measurements.count()
    
    def get_last_measurement(self, obj):
        """Obtener última medición para esta variable"""
        last_measurement = obj.measurements.order_by('-timestamp').first()
        if last_measurement:
            return {
                'timestamp': last_measurement.timestamp,
                'value': last_measurement.value,
                'quality_score': last_measurement.quality_score
            }
        return None

class CatchmentPointSerializer(serializers.ModelSerializer):
    """Serializer para puntos de captación"""
    measurements_count = serializers.SerializerMethodField()
    last_measurement = serializers.SerializerMethodField()
    active_variables = serializers.SerializerMethodField()
    
    class Meta:
        model = CatchmentPoint
        fields = [
            'id', 'project', 'name', 'owner', 'viewers', 'latitude', 'longitude',
            'location', 'frequency', 'is_telemetry_active', 'telemetry_start_date',
            'extra_attributes', 'measurements_count', 'last_measurement',
            'active_variables', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'measurements_count', 'last_measurement', 'active_variables', 'created_at', 'updated_at']
    
    def get_measurements_count(self, obj):
        """Obtener conteo de mediciones para este punto"""
        return obj.measurements.count()
    
    def get_last_measurement(self, obj):
        """Obtener última medición para este punto"""
        last_measurement = obj.measurements.order_by('-timestamp').first()
        if last_measurement:
            return {
                'timestamp': last_measurement.timestamp,
                'variable_name': last_measurement.variable.name,
                'value': last_measurement.value,
                'provider': last_measurement.provider
            }
        return None
    
    def get_active_variables(self, obj):
        """Obtener variables activas para este punto"""
        variables = Variable.objects.filter(
            scheme__catchment_points=obj
        ).distinct()
        
        return [
            {
                'id': var.id,
                'name': var.name,
                'label': var.label,
                'unit': var.unit,
                'variable_type': var.variable_type
            }
            for var in variables
        ]

class SchemeSerializer(serializers.ModelSerializer):
    """Serializer para esquemas"""
    variables_count = serializers.SerializerMethodField()
    points_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Scheme
        fields = [
            'id', 'name', 'description', 'variables_count', 'points_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'variables_count', 'points_count', 'created_at', 'updated_at']
    
    def get_variables_count(self, obj):
        """Obtener conteo de variables en este esquema"""
        return obj.variables.count()
    
    def get_points_count(self, obj):
        """Obtener conteo de puntos que usan este esquema"""
        return obj.catchment_points.count()

class BulkMeasurementSerializer(serializers.Serializer):
    """Serializer para inserción masiva de mediciones"""
    measurements = MeasurementSerializer(many=True)
    batch_id = serializers.CharField(required=False)
    provider = serializers.CharField(required=False)
    frequency = serializers.CharField(required=False)
    
    def validate_measurements(self, value):
        """Validar que no haya demasiadas mediciones"""
        if len(value) > 10000:
            raise serializers.ValidationError("Máximo 10,000 mediciones por lote")
        return value

class MeasurementExportSerializer(serializers.Serializer):
    """Serializer para exportación de mediciones"""
    format = serializers.ChoiceField(choices=['csv', 'json', 'xlsx'], default='csv')
    point_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    variable_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)
    include_raw_data = serializers.BooleanField(default=False)
    include_quality_metrics = serializers.BooleanField(default=False) 