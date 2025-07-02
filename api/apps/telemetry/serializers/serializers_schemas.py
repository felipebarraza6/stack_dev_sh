"""
Serializadores de Esquemas de Telemetría
Serializadores para el sistema basado en esquemas dinámicos
"""
from rest_framework import serializers
from .models_schemas import (
    TelemetrySchema,
    TelemetryGroup,
    TelemetrySchemaMapping,
    TelemetrySchemaProcessor
)
from api.apps.variables.models import Variable
from api.apps.catchment.models import CatchmentPoint


class VariableSerializer(serializers.ModelSerializer):
    """Serializador simplificado para variables"""
    
    class Meta:
        model = Variable
        fields = ['id', 'name', 'code', 'variable_type', 'unit']


class CatchmentPointSerializer(serializers.ModelSerializer):
    """Serializador simplificado para puntos de captación"""
    
    class Meta:
        model = CatchmentPoint
        fields = ['id', 'name', 'code', 'device_id', 'status']


class TelemetrySchemaSerializer(serializers.ModelSerializer):
    """Serializador para esquemas de telemetría"""
    
    variables = VariableSerializer(many=True, read_only=True)
    variables_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Variable.objects.filter(is_active=True),
        source='variables'
    )
    
    class Meta:
        model = TelemetrySchema
        fields = [
            'id', 'name', 'description', 'schema_type', 'variables', 'variables_ids',
            'grouping_config', 'display_config', 'processing_config', 'validation_rules',
            'calculated_fields', 'is_active', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TelemetryGroupSerializer(serializers.ModelSerializer):
    """Serializador para grupos de telemetría"""
    
    schema = TelemetrySchemaSerializer(read_only=True)
    catchment_point = CatchmentPointSerializer(read_only=True)
    
    class Meta:
        model = TelemetryGroup
        fields = [
            'id', 'schema', 'catchment_point', 'timestamp', 'grouped_data',
            'calculated_fields', 'grouping_metadata', 'processing_status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TelemetrySchemaMappingSerializer(serializers.ModelSerializer):
    """Serializador para mapeos de esquemas"""
    
    schema = TelemetrySchemaSerializer(read_only=True)
    catchment_point = CatchmentPointSerializer(read_only=True)
    point_variables = VariableSerializer(many=True, read_only=True)
    
    class Meta:
        model = TelemetrySchemaMapping
        fields = [
            'id', 'schema', 'catchment_point', 'mapping_config', 'point_variables',
            'transformations', 'priority', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TelemetrySchemaProcessorSerializer(serializers.ModelSerializer):
    """Serializador para procesadores de esquemas"""
    
    schemas = TelemetrySchemaSerializer(many=True, read_only=True)
    
    class Meta:
        model = TelemetrySchemaProcessor
        fields = [
            'id', 'name', 'description', 'processor_type', 'schemas',
            'processor_config', 'processor_code', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# Serializadores para endpoints específicos
class TelemetrySchemaSummarySerializer(serializers.Serializer):
    """Serializador para resumen de esquemas"""
    
    total_schemas = serializers.IntegerField()
    schemas_by_type = serializers.DictField()
    active_schemas = serializers.IntegerField()
    total_groups = serializers.IntegerField()


class TelemetryGroupQuerySerializer(serializers.Serializer):
    """Serializador para consultas de grupos"""
    
    schema_name = serializers.CharField(required=False)
    schema_type = serializers.CharField(required=False)
    catchment_point_id = serializers.IntegerField(required=False)
    start_time = serializers.DateTimeField(required=False)
    end_time = serializers.DateTimeField(required=False)
    limit = serializers.IntegerField(default=100, max_value=1000)


class TelemetryGroupResponseSerializer(serializers.Serializer):
    """Serializador para respuestas de grupos"""
    
    schema = TelemetrySchemaSerializer()
    groups = TelemetryGroupSerializer(many=True)
    total_groups = serializers.IntegerField()
    query_params = serializers.DictField()


class TelemetrySchemaCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear esquemas"""
    
    variables_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Variable.objects.filter(is_active=True),
        source='variables'
    )
    
    class Meta:
        model = TelemetrySchema
        fields = [
            'name', 'description', 'schema_type', 'variables_ids',
            'grouping_config', 'display_config', 'processing_config',
            'validation_rules', 'calculated_fields'
        ]
    
    def validate_name(self, value):
        """Validar que el nombre sea único"""
        if TelemetrySchema.objects.filter(name=value).exists():
            raise serializers.ValidationError("Ya existe un esquema con este nombre")
        return value
    
    def validate_grouping_config(self, value):
        """Validar configuración de agrupación"""
        required_fields = ['time_window', 'aggregation']
        for field in required_fields:
            if field not in value:
                raise serializers.ValidationError(f"Campo requerido: {field}")
        return value


class TelemetrySchemaUpdateSerializer(serializers.ModelSerializer):
    """Serializador para actualizar esquemas"""
    
    class Meta:
        model = TelemetrySchema
        fields = [
            'description', 'grouping_config', 'display_config', 'processing_config',
            'validation_rules', 'calculated_fields', 'is_active'
        ]


class TelemetryGroupAggregationSerializer(serializers.Serializer):
    """Serializador para agregaciones de grupos"""
    
    schema_name = serializers.CharField()
    catchment_point_id = serializers.IntegerField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    aggregation_type = serializers.CharField(default='average')
    variables = serializers.ListField(child=serializers.CharField(), required=False)


class TelemetryGroupAggregationResponseSerializer(serializers.Serializer):
    """Serializador para respuestas de agregaciones"""
    
    schema_name = serializers.CharField()
    catchment_point_id = serializers.IntegerField()
    period = serializers.DictField()
    aggregated_data = serializers.DictField()
    statistics = serializers.DictField() 