"""
Serializer para el modelo ProcessedTelemetryData
"""
from rest_framework import serializers
from api.apps.telemetry.models import ProcessedTelemetryData
from api.apps.catchment.models import CatchmentPoint
from api.apps.telemetry.serializers.schemas.response_schema import ResponseSchemaSerializer
from .raw_telemetry_data import RawTelemetryDataSerializer
from .telemetry_data import CatchmentPointSerializer


class ProcessedTelemetryDataSerializer(serializers.ModelSerializer):
    """Serializer para el modelo ProcessedTelemetryData"""
    
    catchment_point = CatchmentPointSerializer(read_only=True)
    response_schema = ResponseSchemaSerializer(read_only=True)
    raw_data = RawTelemetryDataSerializer(read_only=True)
    
    class Meta:
        model = ProcessedTelemetryData
        fields = [
            'id',
            'catchment_point',
            'response_schema',
            'raw_data',
            'measurement_time',
            'processed_data',
            'applied_constants',
            'processing_status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProcessedTelemetryDataListSerializer(serializers.ModelSerializer):
    """Serializer para listar datos procesados de telemetría"""
    
    catchment_point_name = serializers.CharField(source='catchment_point.name', read_only=True)
    response_schema_name = serializers.CharField(source='response_schema.name', read_only=True)
    
    class Meta:
        model = ProcessedTelemetryData
        fields = [
            'id',
            'catchment_point_name',
            'response_schema_name',
            'measurement_time',
            'processing_status',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class ProcessedTelemetryDataDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para el modelo ProcessedTelemetryData"""
    
    catchment_point = CatchmentPointSerializer(read_only=True)
    response_schema = ResponseSchemaSerializer(read_only=True)
    
    class Meta:
        model = ProcessedTelemetryData
        fields = [
            'id',
            'catchment_point',
            'response_schema',
            'measurement_time',
            'processed_data',
            'applied_constants',
            'processing_status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 