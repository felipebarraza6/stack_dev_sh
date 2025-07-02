"""
Serializer para el modelo TelemetryData
"""
from rest_framework import serializers
from api.apps.telemetry.models import TelemetryData
from api.apps.catchment.models import CatchmentPoint


class CatchmentPointSerializer(serializers.ModelSerializer):
    """Serializer simplificado para puntos de captación"""
    
    class Meta:
        model = CatchmentPoint
        fields = ['id', 'name', 'code', 'device_id', 'status']


class TelemetryDataSerializer(serializers.ModelSerializer):
    """Serializer para el modelo TelemetryData"""
    
    catchment_point = CatchmentPointSerializer(read_only=True)
    catchment_point_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = TelemetryData
        fields = [
            'id',
            'catchment_point',
            'catchment_point_id',
            'measurement_time',
            'logger_time',
            'flow',
            'total',
            'total_diff',
            'total_today_diff',
            'level',
            'water_table',
            'pulses',
            'days_not_connection',
            'send_dga',
            'dga_response',
            'dga_voucher',
            'is_warning',
            'is_error',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TelemetryDataListSerializer(serializers.ModelSerializer):
    """Serializer para listar datos de telemetría"""
    
    catchment_point_name = serializers.CharField(source='catchment_point.name', read_only=True)
    
    class Meta:
        model = TelemetryData
        fields = [
            'id',
            'catchment_point_name',
            'measurement_time',
            'flow',
            'total',
            'level',
            'water_table',
            'is_warning',
            'is_error',
            'send_dga',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class TelemetryDataDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para el modelo TelemetryData"""
    
    catchment_point = CatchmentPointSerializer(read_only=True)
    
    class Meta:
        model = TelemetryData
        fields = [
            'id',
            'catchment_point',
            'measurement_time',
            'logger_time',
            'flow',
            'total',
            'total_diff',
            'total_today_diff',
            'level',
            'water_table',
            'pulses',
            'days_not_connection',
            'send_dga',
            'dga_response',
            'dga_voucher',
            'is_warning',
            'is_error',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 