"""
Serializers for the Ticket model.
"""
from rest_framework import serializers
from api.apps.support.models import Ticket, Department

class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ticket model, including a dynamic field for connection status.
    """
    connection_status = serializers.SerializerMethodField()
    department_name = serializers.CharField(source='department.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description', 'status', 'priority', 'resolution_notes',
            'department', 'department_name',
            'created_by', 'created_by_username',
            'assigned_to', 'assigned_to_username',
            'catchment_point', 'project',
            'connection_status', # Our dynamic field
            'created_at', 'updated_at', 'image'
        ]
        # Make department writable by its ID, but show its name when reading
        read_only_fields = ['department_name', 'created_by_username', 'assigned_to_username']
        extra_kwargs = {
            'department': {'write_only': True, 'required': False, 'allow_null': True},
            'created_by': {'write_only': True, 'required': False, 'allow_null': True},
            'assigned_to': {'write_only': True, 'required': False, 'allow_null': True},
        }

    def get_connection_status(self, obj):
        """
        Calls the model's method to get the real-time connection status.
        """
        return obj.get_connection_status()

    def to_representation(self, instance):
        """
        Customize the output representation.
        """
        representation = super().to_representation(instance)
        # Ensure department_name is fetched for read operations
        representation['department_name'] = instance.department.name if instance.department else None
        return representation 