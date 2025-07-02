"""
Serializador de Notificaciones de Puntos de Captación
"""
from rest_framework import serializers
from api.apps.catchment.models.notifications import NotificationsCatchment
from ..points.catchment_point import CatchmentPointSerializer


class NotificationsCatchmentSerializer(serializers.ModelSerializer):
    """Serializador para notificaciones de puntos de captación"""
    
    point_catchment = CatchmentPointSerializer(read_only=True)
    point_catchment_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = NotificationsCatchment
        fields = [
            'id', 'point_catchment', 'point_catchment_id',
            'type_variable', 'type_notification', 'message',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 