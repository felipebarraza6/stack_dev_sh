"""
Serializador de Alertas de Variables
"""
from rest_framework import serializers
from api.apps.variables.models.alerts import VariableAlert
from ..variables.variable import VariableSerializer


class VariableAlertSerializer(serializers.ModelSerializer):
    """Serializador para alertas de variables"""
    
    variable = VariableSerializer(read_only=True)
    variable_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = VariableAlert
        fields = [
            'id', 'variable', 'variable_id', 'name', 'description',
            'alert_type', 'severity', 'alert_config', 'conditions',
            'actions', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 