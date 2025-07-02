"""
Serializer para el modelo ResponseSchema
"""
from rest_framework import serializers
from api.apps.telemetry.models import ResponseSchema


class ResponseSchemaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo ResponseSchema"""
    
    class Meta:
        model = ResponseSchema
        fields = [
            'id',
            'name',
            'description',
            'schema_type',
            'schema_definition',
            'processing_config',
            'included_variables',
            'transformations',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ResponseSchemaListSerializer(serializers.ModelSerializer):
    """Serializer para listar esquemas de respuesta"""
    
    class Meta:
        model = ResponseSchema
        fields = [
            'id',
            'name',
            'description',
            'schema_type',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class ResponseSchemaDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para el modelo ResponseSchema"""
    
    class Meta:
        model = ResponseSchema
        fields = [
            'id',
            'name',
            'description',
            'schema_type',
            'schema_definition',
            'processing_config',
            'included_variables',
            'transformations',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 