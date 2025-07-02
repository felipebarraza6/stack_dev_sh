"""
Serializer para el modelo ComplianceConfig
"""
from rest_framework import serializers
from api.apps.compliance.models import ComplianceConfig, ComplianceSource
from ..sources.compliance_source import ComplianceSourceSerializer


class ComplianceConfigSerializer(serializers.ModelSerializer):
    """Serializer para el modelo ComplianceConfig"""
    
    compliance_source = ComplianceSourceSerializer(read_only=True)
    compliance_source_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ComplianceConfig
        fields = [
            'id',
            'catchment_point',
            'compliance_source',
            'compliance_source_id',
            'config',
            'is_active',
            'start_date',
            'end_date',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_compliance_source_id(self, value):
        """Validar que la fuente de cumplimiento existe"""
        if not ComplianceSource.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("La fuente de cumplimiento no existe o no está activa.")
        return value


class ComplianceConfigListSerializer(serializers.ModelSerializer):
    """Serializer para listar configuraciones de cumplimiento"""
    
    compliance_source_name = serializers.CharField(source='compliance_source.name', read_only=True)
    catchment_point_name = serializers.CharField(source='catchment_point.name', read_only=True)
    
    class Meta:
        model = ComplianceConfig
        fields = [
            'id',
            'catchment_point_name',
            'compliance_source_name',
            'is_active',
            'start_date',
            'end_date',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class ComplianceConfigDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para el modelo ComplianceConfig"""
    
    compliance_source = ComplianceSourceSerializer(read_only=True)
    
    class Meta:
        model = ComplianceConfig
        fields = [
            'id',
            'catchment_point',
            'compliance_source',
            'config',
            'is_active',
            'start_date',
            'end_date',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 