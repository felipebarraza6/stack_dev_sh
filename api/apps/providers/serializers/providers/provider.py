"""
Serializer para el modelo Provider
"""
from rest_framework import serializers
from ...models import Provider


class ProviderSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Provider"""
    
    class Meta:
        model = Provider
        fields = [
            'id',
            'name',
            'description',
            'provider_type',
            'connection_config',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        """Validar que el nombre sea único"""
        if Provider.objects.filter(name=value).exists():
            raise serializers.ValidationError("Ya existe un proveedor con este nombre.")
        return value


class ProviderListSerializer(serializers.ModelSerializer):
    """Serializer para listar proveedores"""
    
    class Meta:
        model = Provider
        fields = [
            'id',
            'name',
            'provider_type',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class ProviderDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para el modelo Provider"""
    
    class Meta:
        model = Provider
        fields = [
            'id',
            'name',
            'description',
            'provider_type',
            'connection_config',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 