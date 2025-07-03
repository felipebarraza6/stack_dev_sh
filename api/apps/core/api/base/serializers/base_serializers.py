"""
Serializers Base para API Interna
Proporciona serializers base sin lógica de frontend
"""
from rest_framework import serializers
from api.apps.core.models import BaseModel


class BaseModelSerializer(serializers.ModelSerializer):
    """Serializer base para modelos que heredan de BaseModel"""
    
    class Meta:
        abstract = True
        fields = ['id', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['id', 'created_at', 'updated_at']


class BaseViewSetSerializer(BaseModelSerializer):
    """Serializer base para ViewSets de la API interna"""
    
    class Meta(BaseModelSerializer.Meta):
        abstract = True


class VariableBaseSerializer(BaseViewSetSerializer):
    """Serializer base para variables (sin lógica de frontend)"""
    
    class Meta(BaseViewSetSerializer.Meta):
        from api.apps.variables.models.variables.variable import Variable
        model = Variable
        fields = BaseViewSetSerializer.Meta.fields + [
            'name', 'code', 'variable_type', 'unit', 'custom_unit',
            'processing_config', 'min_value', 'max_value', 'alert_config'
        ]


class VariableSchemaBaseSerializer(BaseViewSetSerializer):
    """Serializer base para esquemas de variables"""
    
    class Meta(BaseViewSetSerializer.Meta):
        from api.apps.variables.models.schemas.schema import VariableSchema
        model = VariableSchema
        fields = BaseViewSetSerializer.Meta.fields + [
            'name', 'description', 'schema_definition', 'variables',
            'processing_config', 'validation_rules'
        ]


class CatchmentPointBaseSerializer(BaseViewSetSerializer):
    """Serializer base para puntos de captación"""
    
    class Meta(BaseViewSetSerializer.Meta):
        from api.apps.catchment.models.points.catchment_point import CatchmentPoint
        model = CatchmentPoint
        fields = BaseViewSetSerializer.Meta.fields + [
            'name', 'code', 'point_type', 'owner', 'latitude', 'longitude',
            'altitude', 'device_id', 'provider', 'config', 'status',
            'sampling_frequency'
        ]


class TelemetryDataBaseSerializer(BaseViewSetSerializer):
    """Serializer base para datos de telemetría"""
    
    class Meta(BaseViewSetSerializer.Meta):
        from api.apps.telemetry.models.data.telemetry_data import TelemetryData
        model = TelemetryData
        fields = BaseViewSetSerializer.Meta.fields + [
            'catchment_point', 'measurement_time', 'logger_time',
            'level', 'water_table', 'flow', 'temperature', 'pressure',
            'ph', 'conductivity', 'turbidity', 'battery_level',
            'signal_strength', 'days_not_connection', 'send_dga',
            'dga_response', 'dga_voucher', 'is_warning', 'is_error'
        ] 