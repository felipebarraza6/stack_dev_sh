"""
Serializador de Puntos de Captación
"""
from rest_framework import serializers
from api.apps.catchment.models.points import CatchmentPoint
from api.apps.users.models.users import User


class UserSerializer(serializers.ModelSerializer):
    """Serializador simplificado para usuarios"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CatchmentPointSerializer(serializers.ModelSerializer):
    """Serializador para puntos de captación"""
    
    owner = UserSerializer(read_only=True)
    owner_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = CatchmentPoint
        fields = [
            'id', 'name', 'code', 'point_type', 'owner', 'owner_id',
            'latitude', 'longitude', 'altitude', 'device_id', 'provider',
            'config', 'status', 'is_active', 'sampling_frequency',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 