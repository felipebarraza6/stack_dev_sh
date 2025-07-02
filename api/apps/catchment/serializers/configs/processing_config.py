"""
Serializador de Configuración de Procesamiento
"""
from rest_framework import serializers
from api.apps.catchment.models.configs import CatchmentPointProcessingConfig
from ..points.catchment_point import CatchmentPointSerializer


class CatchmentPointProcessingConfigSerializer(serializers.ModelSerializer):
    """Serializador para configuración de procesamiento"""
    
    catchment_point = CatchmentPointSerializer(read_only=True)
    catchment_point_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = CatchmentPointProcessingConfig
        fields = [
            'id', 'catchment_point', 'catchment_point_id',
            'pump_position', 'level_position', 'depth', 'pipe_diameter',
            'flowmeter_diameter', 'additional_config', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 