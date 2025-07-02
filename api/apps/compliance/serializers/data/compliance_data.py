"""
Serializer para el modelo ComplianceData
"""
from rest_framework import serializers
from api.apps.compliance.models import ComplianceData, ComplianceConfig


class ComplianceDataSerializer(serializers.ModelSerializer):
    """Serializer para el modelo ComplianceData"""
    
    compliance_config_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ComplianceData
        fields = [
            'id',
            'compliance_config',
            'compliance_config_id',
            'data',
            'status',
            'response',
            'sent_at',
            'confirmed_at'
        ]
        read_only_fields = ['id', 'sent_at', 'confirmed_at']
    
    def validate_compliance_config_id(self, value):
        """Validar que la configuración de cumplimiento existe"""
        if not ComplianceConfig.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("La configuración de cumplimiento no existe o no está activa.")
        return value


class ComplianceDataListSerializer(serializers.ModelSerializer):
    """Serializer para listar datos de cumplimiento"""
    
    compliance_config_info = serializers.SerializerMethodField()
    
    class Meta:
        model = ComplianceData
        fields = [
            'id',
            'compliance_config_info',
            'status',
            'sent_at',
            'confirmed_at'
        ]
        read_only_fields = ['id', 'sent_at', 'confirmed_at']
    
    def get_compliance_config_info(self, obj):
        """Obtener información básica de la configuración"""
        return {
            'id': obj.compliance_config.id,
            'catchment_point': obj.compliance_config.catchment_point.name,
            'source': obj.compliance_config.compliance_source.name
        }


class ComplianceDataDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para el modelo ComplianceData"""
    
    class Meta:
        model = ComplianceData
        fields = [
            'id',
            'compliance_config',
            'data',
            'status',
            'response',
            'sent_at',
            'confirmed_at'
        ]
        read_only_fields = ['id', 'sent_at', 'confirmed_at'] 