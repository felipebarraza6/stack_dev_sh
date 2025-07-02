"""
Serializer para el modelo DataSchema
"""
from rest_framework import serializers
from ...models import DataSchema


class DataSchemaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo DataSchema"""
    
    class Meta:
        model = DataSchema
        fields = [
            'id',
            'name',
            'description',
            'schema_definition',
            'supported_variables',
            'processing_rules',
            'validation_rules',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        """Validar que el nombre sea único"""
        if DataSchema.objects.filter(name=value).exists():
            raise serializers.ValidationError("Ya existe un esquema con este nombre.")
        return value
    
    def validate_schema_definition(self, value):
        """Validar que la definición del esquema sea válida"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("La definición del esquema debe ser un objeto JSON válido.")
        return value


class DataSchemaListSerializer(serializers.ModelSerializer):
    """Serializer para listar esquemas de datos"""
    
    class Meta:
        model = DataSchema
        fields = [
            'id',
            'name',
            'description',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class DataSchemaDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para el modelo DataSchema"""
    
    class Meta:
        model = DataSchema
        fields = [
            'id',
            'name',
            'description',
            'schema_definition',
            'supported_variables',
            'processing_rules',
            'validation_rules',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 