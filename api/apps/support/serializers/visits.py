"""
Serializers for the FieldVisit model.
"""
from rest_framework import serializers
from api.apps.support.models import FieldVisit

class FieldVisitSerializer(serializers.ModelSerializer):
    """
    Serializer for the FieldVisit model.
    """
    technician_username = serializers.CharField(source='technician.username', read_only=True)

    class Meta:
        model = FieldVisit
        fields = [
            'id', 'ticket', 'technician', 'technician_username',
            'scheduled_date', 'start_time', 'end_time',
            'status', 'visit_report',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['technician_username']
        extra_kwargs = {
            'technician': {'write_only': True, 'required': False, 'allow_null': True},
        } 