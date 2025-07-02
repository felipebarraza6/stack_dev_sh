"""
Serializer para el modelo ComplianceSource
"""
from rest_framework import serializers
from api.apps.compliance.models import ComplianceSource


class ComplianceSourceSerializer(serializers.ModelSerializer):
    """Serializer para el modelo ComplianceSource"""
    
    class Meta:
        model = ComplianceSource
        fields = [
            'id',
            'name',
            'code',
            'description',
            'config',
            'supported_variables',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        """Validar que el nombre sea único"""
        if ComplianceSource.objects.filter(name=value).exists():
            raise serializers.ValidationError("Ya existe una fuente con este nombre.")
        return value
    
    def validate_code(self, value):
        """Validar que el código sea único"""
        if ComplianceSource.objects.filter(code=value).exists():
            raise serializers.ValidationError("Ya existe una fuente con este código.")
        return value


class ComplianceSourceListSerializer(serializers.ModelSerializer):
    """Serializer para listar fuentes de cumplimiento"""
    
    class Meta:
        model = ComplianceSource
        fields = [
            'id',
            'name',
            'code',
            'description',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class ComplianceSourceDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para el modelo ComplianceSource"""
    
    class Meta:
        model = ComplianceSource
        fields = [
            'id',
            'name',
            'code',
            'description',
            'config',
            'supported_variables',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 