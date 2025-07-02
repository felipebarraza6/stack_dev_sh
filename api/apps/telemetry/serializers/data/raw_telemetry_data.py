"""
Serializer para el modelo RawTelemetryData
"""
from rest_framework import serializers
from api.apps.telemetry.models import RawTelemetryData
from api.apps.catchment.models import CatchmentPoint


class RawTelemetryDataSerializer(serializers.ModelSerializer):
    """Serializer para el modelo RawTelemetryData"""
    
    catchment_point = CatchmentPointSerializer(read_only=True)
    catchment_point_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = RawTelemetryData
        fields = [
            'id',
            'catchment_point',
            'catchment_point_id',
            'measurement_time',
            'logger_time',
            'raw_data',
            'is_processed',
            'processing_status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RawTelemetryDataListSerializer(serializers.ModelSerializer):
    """Serializer para listar datos brutos de telemetría"""
    
    catchment_point_name = serializers.CharField(source='catchment_point.name', read_only=True)
    
    class Meta:
        model = RawTelemetryData
        fields = [
            'id',
            'catchment_point_name',
            'measurement_time',
            'is_processed',
            'processing_status',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class RawTelemetryDataDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para el modelo RawTelemetryData"""
    
    catchment_point = CatchmentPointSerializer(read_only=True)
    
    class Meta:
        model = RawTelemetryData
        fields = [
            'id',
            'catchment_point',
            'measurement_time',
            'logger_time',
            'raw_data',
            'is_processed',
            'processing_status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 