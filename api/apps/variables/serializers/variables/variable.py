"""
Serializador de Variables
"""
from rest_framework import serializers
from api.apps.variables.models.variables import Variable


class VariableSerializer(serializers.ModelSerializer):
    """Serializador para variables"""
    
    class Meta:
        model = Variable
        fields = [
            'id', 'name', 'code', 'variable_type', 'unit', 'custom_unit',
            'processing_config', 'min_value', 'max_value', 'alert_config',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 