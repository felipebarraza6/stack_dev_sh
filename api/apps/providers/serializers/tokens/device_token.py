"""
Serializer para el modelo DeviceToken
"""
from rest_framework import serializers
from ...models import DeviceToken


class DeviceTokenSerializer(serializers.ModelSerializer):
    """Serializer para el modelo DeviceToken"""
    
    class Meta:
        model = DeviceToken
        fields = [
            'id',
            'device_id',
            'token',
            'is_active',
            'expires_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'token', 'created_at', 'updated_at']
        extra_kwargs = {
            'token': {'write_only': True}
        }
    
    def validate_device_id(self, value):
        """Validar que el device_id sea único"""
        if DeviceToken.objects.filter(device_id=value, is_active=True).exists():
            raise serializers.ValidationError("Ya existe un token activo para este dispositivo.")
        return value


class DeviceTokenListSerializer(serializers.ModelSerializer):
    """Serializer para listar tokens de dispositivos"""
    
    class Meta:
        model = DeviceToken
        fields = [
            'id',
            'device_id',
            'is_active',
            'expires_at',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class DeviceTokenDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para el modelo DeviceToken"""
    
    class Meta:
        model = DeviceToken
        fields = [
            'id',
            'device_id',
            'is_active',
            'expires_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 