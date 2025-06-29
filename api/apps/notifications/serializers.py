"""
Serializers para la API de notificaciones
"""
from rest_framework import serializers
from .models import (
    NotificationTemplate, Notification, NotificationPreference, NotificationLog
)


class NotificationTemplateSerializer(serializers.ModelSerializer):
    """Serializer para plantillas de notificación"""
    
    class Meta:
        model = NotificationTemplate
        fields = [
            'id', 'name', 'module', 'notification_type', 'subject',
            'message_template', 'is_active', 'available_variables',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer para notificaciones"""
    template_name = serializers.CharField(source='template.name', read_only=True)
    module = serializers.CharField(source='template.module', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'subject', 'message', 'status', 'priority',
            'related_model', 'related_id', 'sent_at', 'read_at',
            'template_name', 'module', 'metadata', 'created_at'
        ]
        read_only_fields = [
            'subject', 'message', 'status', 'priority',
            'related_model', 'related_id', 'sent_at', 'read_at',
            'template_name', 'module', 'metadata', 'created_at'
        ]


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Serializer para preferencias de notificación"""
    
    class Meta:
        model = NotificationPreference
        fields = [
            'id', 'module', 'email_enabled', 'websocket_enabled',
            'settings', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class NotificationLogSerializer(serializers.ModelSerializer):
    """Serializer para logs de notificación"""
    
    class Meta:
        model = NotificationLog
        fields = [
            'id', 'channel', 'status', 'sent_at', 'error_message',
            'delivery_data', 'created_at'
        ]
        read_only_fields = ['created_at']


class NotificationStatsSerializer(serializers.Serializer):
    """Serializer para estadísticas de notificaciones"""
    total_notifications = serializers.IntegerField()
    unread_notifications = serializers.IntegerField()
    notifications_by_module = serializers.DictField()
    notifications_by_status = serializers.DictField()
    notifications_by_priority = serializers.DictField()


class NotificationBulkActionSerializer(serializers.Serializer):
    """Serializer para acciones masivas en notificaciones"""
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )
    action = serializers.ChoiceField(choices=[
        'mark_read', 'mark_unread', 'delete'
    ])


class NotificationFilterSerializer(serializers.Serializer):
    """Serializer para filtros de notificaciones"""
    module = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    priority = serializers.CharField(required=False)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    unread_only = serializers.BooleanField(default=False) 