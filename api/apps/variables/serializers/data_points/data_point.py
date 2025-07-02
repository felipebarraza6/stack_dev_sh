"""
Serializador de Puntos de Datos de Variables
"""
from rest_framework import serializers
from api.apps.variables.models.data_points import VariableDataPoint
from ..variables.variable import VariableSerializer


class VariableDataPointSerializer(serializers.ModelSerializer):
    """Serializador para puntos de datos de variables"""
    
    variable = VariableSerializer(read_only=True)
    variable_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = VariableDataPoint
        fields = [
            'id', 'variable', 'variable_id', 'catchment_point_id', 'value',
            'timestamp', 'quality', 'metadata', 'is_processed',
            'processing_status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 