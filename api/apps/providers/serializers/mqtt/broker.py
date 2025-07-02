"""
Serializer para el modelo MQTTBroker
"""
from rest_framework import serializers
from ...models import MQTTBroker


class MQTTBrokerSerializer(serializers.ModelSerializer):
    """Serializer para el modelo MQTTBroker"""
    
    class Meta:
        model = MQTTBroker
        fields = [
            'id',
            'name',
            'host',
            'port',
            'username',
            'password',
            'use_tls',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_host(self, value):
        """Validar formato del host"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("El host no puede estar vacío.")
        return value.strip()
    
    def validate_port(self, value):
        """Validar rango del puerto"""
        if value < 1 or value > 65535:
            raise serializers.ValidationError("El puerto debe estar entre 1 y 65535.")
        return value


class MQTTBrokerListSerializer(serializers.ModelSerializer):
    """Serializer para listar brokers MQTT"""
    
    class Meta:
        model = MQTTBroker
        fields = [
            'id',
            'name',
            'host',
            'port',
            'use_tls',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class MQTTBrokerDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para el modelo MQTTBroker"""
    
    class Meta:
        model = MQTTBroker
        fields = [
            'id',
            'name',
            'host',
            'port',
            'username',
            'use_tls',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        } 