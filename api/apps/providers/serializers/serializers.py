"""
Serializadores de Proveedores
Serializadores para los modelos de providers
"""
from rest_framework import serializers
from .models import Provider, MQTTBroker, DeviceToken, DataSchema, DataIngestionLog


class ProviderSerializer(serializers.ModelSerializer):
    """Serializador para proveedores"""
    
    class Meta:
        model = Provider
        fields = [
            'id', 'name', 'code', 'provider_type', 'description',
            'api_endpoint', 'api_version', 'authentication_config',
            'data_format', 'connection_config', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MQTTBrokerSerializer(serializers.ModelSerializer):
    """Serializador para configuración MQTT"""
    
    provider = ProviderSerializer(read_only=True)
    provider_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = MQTTBroker
        fields = [
            'id', 'provider', 'provider_id', 'broker_host', 'broker_port',
            'use_tls', 'username', 'password', 'keepalive', 'reconnect_delay',
            'topic_prefix', 'topic_pattern', 'qos_level'
        ]
        read_only_fields = ['id']


class DeviceTokenSerializer(serializers.ModelSerializer):
    """Serializador para tokens de dispositivos"""
    
    provider = ProviderSerializer(read_only=True)
    provider_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = DeviceToken
        fields = [
            'id', 'provider', 'provider_id', 'device_id', 'token',
            'token_type', 'expires_at', 'is_active', 'created_at', 'last_used'
        ]
        read_only_fields = ['id', 'created_at', 'last_used']


# Serializadores para endpoints específicos
class ProviderSummarySerializer(serializers.Serializer):
    """Serializador para resumen de proveedores"""
    
    total_providers = serializers.IntegerField()
    active_providers = serializers.IntegerField()
    providers_by_type = serializers.DictField()
    connection_stats = serializers.DictField()


class ProviderStatusSerializer(serializers.Serializer):
    """Serializador para estado de proveedores"""
    
    provider = ProviderSerializer()
    mqtt_config = MQTTBrokerSerializer()
    device_tokens = DeviceTokenSerializer(many=True)
    health_status = serializers.DictField() 