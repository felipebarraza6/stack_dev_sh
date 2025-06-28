"""
Serializers for Telemetry models.
"""
from rest_framework import serializers
from .models.points import CatchmentPoint, InteractionDetail
from .models.schemes import Scheme, Variable

class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable
        fields = '__all__'

class SchemeSerializer(serializers.ModelSerializer):
    variables = VariableSerializer(many=True, read_only=True)

    class Meta:
        model = Scheme
        fields = ['id', 'name', 'description', 'catchment_points', 'variables']

class CatchmentPointSerializer(serializers.ModelSerializer):
    # Making nested relationships read-only to simplify writes.
    # Full details can be fetched from their own endpoints.
    owner = serializers.StringRelatedField(read_only=True)
    project = serializers.StringRelatedField(read_only=True)
    schemes = SchemeSerializer(many=True, read_only=True)
    
    class Meta:
        model = CatchmentPoint
        fields = [
            'id', 'name', 'owner', 'project', 'latitude', 'longitude', 
            'is_telemetry_active', 'telemetry_start_date', 'frequency',
            'extra_attributes', 'schemes'
        ]

class InteractionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteractionDetail
        fields = '__all__' 