"""
Serializadores de Telemetría
Serializadores para los modelos de telemetría mejorados
"""
from rest_framework import serializers
from .models import (
    TelemetryData,
    RawTelemetryData,
    ProcessedTelemetryData,
    ResponseSchema,
    ProcessingConstant,
    TelemetryNotification,
    TelemetryProcessingLog
)
from api.apps.catchment.models import CatchmentPoint


class CatchmentPointSerializer(serializers.ModelSerializer):
    """Serializador simplificado para puntos de captación"""
    
    class Meta:
        model = CatchmentPoint
        fields = ['id', 'name', 'code', 'device_id', 'status']


class TelemetryDataSerializer(serializers.ModelSerializer):
    """Serializador para datos de telemetría"""
    
    catchment_point = CatchmentPointSerializer(read_only=True)
    catchment_point_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = TelemetryData
        fields = [
            'id', 'catchment_point', 'catchment_point_id',
            'measurement_time', 'logger_time', 'flow', 'total',
            'total_diff', 'total_today_diff', 'level', 'water_table',
            'pulses', 'days_not_connection', 'send_dga', 'dga_response',
            'dga_voucher', 'is_warning', 'is_error', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RawTelemetryDataSerializer(serializers.ModelSerializer):
    """Serializador para datos brutos de telemetría"""
    
    catchment_point = CatchmentPointSerializer(read_only=True)
    catchment_point_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = RawTelemetryData
        fields = [
            'id', 'catchment_point', 'catchment_point_id',
            'measurement_time', 'logger_time', 'raw_data',
            'is_processed', 'processing_status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ResponseSchemaSerializer(serializers.ModelSerializer):
    """Serializador para esquemas de respuesta"""
    
    class Meta:
        model = ResponseSchema
        fields = [
            'id', 'name', 'description', 'schema_type',
            'schema_definition', 'processing_config', 'included_variables',
            'transformations', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProcessingConstantSerializer(serializers.ModelSerializer):
    """Serializador para constantes de procesamiento"""
    
    catchment_points = CatchmentPointSerializer(many=True, read_only=True)
    variables = serializers.SerializerMethodField()
    
    class Meta:
        model = ProcessingConstant
        fields = [
            'id', 'name', 'description', 'constant_type', 'value',
            'start_date', 'end_date', 'config', 'catchment_points',
            'variables', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_variables(self, obj):
        """Obtener información de variables relacionadas"""
        return [
            {
                'id': var.id,
                'name': var.name,
                'code': var.code,
                'variable_type': var.variable_type
            }
            for var in obj.variables.all()
        ]


class ProcessedTelemetryDataSerializer(serializers.ModelSerializer):
    """Serializador para datos procesados de telemetría"""
    
    catchment_point = CatchmentPointSerializer(read_only=True)
    response_schema = ResponseSchemaSerializer(read_only=True)
    raw_data = RawTelemetryDataSerializer(read_only=True)
    
    class Meta:
        model = ProcessedTelemetryData
        fields = [
            'id', 'catchment_point', 'response_schema', 'raw_data',
            'measurement_time', 'processed_data', 'applied_constants',
            'processing_status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TelemetryNotificationSerializer(serializers.ModelSerializer):
    """Serializador para notificaciones de telemetría"""
    
    catchment_point = CatchmentPointSerializer(read_only=True)
    
    class Meta:
        model = TelemetryNotification
        fields = [
            'id', 'catchment_point', 'title', 'message',
            'notification_type', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TelemetryProcessingLogSerializer(serializers.ModelSerializer):
    """Serializador para logs de procesamiento"""
    
    catchment_point = CatchmentPointSerializer(read_only=True)
    
    class Meta:
        model = TelemetryProcessingLog
        fields = [
            'id', 'catchment_point', 'log_type', 'message',
            'details', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


# Serializadores para endpoints específicos
class TelemetryDashboardSerializer(serializers.Serializer):
    """Serializador para datos del dashboard"""
    
    statistics = serializers.DictField()
    latest_records = TelemetryDataSerializer(many=True)
    filters_applied = serializers.DictField()


class TelemetryMonthlySummarySerializer(serializers.Serializer):
    """Serializador para resumen mensual"""
    
    period = serializers.DictField()
    points_summary = serializers.ListField()
    total_points = serializers.IntegerField()


class TelemetryPointDetailsSerializer(serializers.Serializer):
    """Serializador para detalles de punto"""
    
    catchment_point = serializers.DictField()
    statistics = serializers.DictField()
    daily_trends = serializers.ListField()
    period = serializers.DictField()


class TelemetryAlertsSerializer(serializers.Serializer):
    """Serializador para alertas"""
    
    alerts = TelemetryDataSerializer(many=True)
    total_alerts = serializers.IntegerField()
    period = serializers.DictField()


class TelemetrySystemStatusSerializer(serializers.Serializer):
    """Serializador para estado del sistema"""
    
    system_info = serializers.DictField()
    configuration = serializers.DictField()
    latest_activity = TelemetryDataSerializer(many=True) 