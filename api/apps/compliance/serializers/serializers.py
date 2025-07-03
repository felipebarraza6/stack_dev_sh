"""
Serializadores de Compliance
Serializadores para los modelos de compliance
"""
from rest_framework import serializers
from api.apps.compliance.models.sources.compliance_source import ComplianceSource
from api.apps.compliance.models.configs.compliance_config import ComplianceConfig
from api.apps.compliance.models.data.compliance_data import ComplianceData
from api.apps.compliance.models.logs.compliance_log import ComplianceLog


class ComplianceSourceSerializer(serializers.ModelSerializer):
    """Serializador para fuentes de cumplimiento"""
    
    class Meta:
        model = ComplianceSource
        fields = [
            'id', 'name', 'code', 'description', 'config',
            'supported_variables', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ComplianceConfigSerializer(serializers.ModelSerializer):
    """Serializador para configuración de cumplimiento"""
    
    compliance_source = ComplianceSourceSerializer(read_only=True)
    compliance_source_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ComplianceConfig
        fields = [
            'id', 'catchment_point', 'compliance_source', 'compliance_source_id',
            'config', 'is_active', 'start_date', 'end_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ComplianceDataSerializer(serializers.ModelSerializer):
    """Serializador para datos de cumplimiento"""
    
    compliance_config = ComplianceConfigSerializer(read_only=True)
    compliance_config_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ComplianceData
        fields = [
            'id', 'compliance_config', 'compliance_config_id', 'data',
            'status', 'response', 'sent_at', 'confirmed_at'
        ]
        read_only_fields = ['id', 'sent_at', 'confirmed_at']


# Serializadores para endpoints específicos
class ComplianceSummarySerializer(serializers.Serializer):
    """Serializador para resumen de cumplimiento"""
    
    total_sources = serializers.IntegerField()
    active_sources = serializers.IntegerField()
    data_sent_count = serializers.IntegerField()
    success_rate = serializers.FloatField()


class ComplianceDataSummarySerializer(serializers.Serializer):
    """Serializador para resumen de datos de cumplimiento"""
    
    total_data = serializers.IntegerField()
    sent_data = serializers.IntegerField()
    confirmed_data = serializers.IntegerField()
    rejected_data = serializers.IntegerField() 