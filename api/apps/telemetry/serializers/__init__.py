"""
Serializers de Telemetría
"""
from rest_framework import serializers

from .data import (
    TelemetryDataSerializer,
    TelemetryDataListSerializer,
    TelemetryDataDetailSerializer,
    RawTelemetryDataSerializer,
    RawTelemetryDataListSerializer,
    RawTelemetryDataDetailSerializer,
    ProcessedTelemetryDataSerializer,
    ProcessedTelemetryDataListSerializer,
    ProcessedTelemetryDataDetailSerializer,
    CatchmentPointSerializer,
)

from .schemas import (
    ResponseSchemaSerializer,
    ResponseSchemaListSerializer,
    ResponseSchemaDetailSerializer,
)

# Serializers para endpoints específicos
class TelemetryDashboardSerializer(serializers.Serializer):
    """Serializer para datos del dashboard"""
    
    statistics = serializers.DictField()
    latest_records = TelemetryDataSerializer(many=True)
    filters_applied = serializers.DictField()


class TelemetryMonthlySummarySerializer(serializers.Serializer):
    """Serializer para resumen mensual"""
    
    period = serializers.DictField()
    points_summary = serializers.ListField()
    total_points = serializers.IntegerField()


class TelemetryPointDetailsSerializer(serializers.Serializer):
    """Serializer para detalles de punto"""
    
    catchment_point = serializers.DictField()
    statistics = serializers.DictField()
    daily_trends = serializers.ListField()
    period = serializers.DictField()


class TelemetryAlertsSerializer(serializers.Serializer):
    """Serializer para alertas"""
    
    alerts = TelemetryDataSerializer(many=True)
    total_alerts = serializers.IntegerField()
    period = serializers.DictField()


class TelemetrySystemStatusSerializer(serializers.Serializer):
    """Serializer para estado del sistema"""
    
    system_info = serializers.DictField()
    configuration = serializers.DictField()
    latest_activity = TelemetryDataSerializer(many=True)

__all__ = [
    # Data
    'TelemetryDataSerializer',
    'TelemetryDataListSerializer',
    'TelemetryDataDetailSerializer',
    'RawTelemetryDataSerializer',
    'RawTelemetryDataListSerializer',
    'RawTelemetryDataDetailSerializer',
    'ProcessedTelemetryDataSerializer',
    'ProcessedTelemetryDataListSerializer',
    'ProcessedTelemetryDataDetailSerializer',
    'CatchmentPointSerializer',
    
    # Schemas
    'ResponseSchemaSerializer',
    'ResponseSchemaListSerializer',
    'ResponseSchemaDetailSerializer',
    
    # Dashboard
    'TelemetryDashboardSerializer',
    'TelemetryMonthlySummarySerializer',
    'TelemetryPointDetailsSerializer',
    'TelemetryAlertsSerializer',
    'TelemetrySystemStatusSerializer',
]
