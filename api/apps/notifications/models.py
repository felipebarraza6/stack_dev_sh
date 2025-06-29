"""
Modelos para el sistema de notificaciones de SmartHydro
"""
from django.db import models
from django.conf import settings
from api.apps.common.models import BaseModel


class NotificationTemplate(BaseModel):
    """
    Plantillas de notificaciones configurables por módulo
    """
    class Module(models.TextChoices):
        BANKING = 'banking', 'Banking'
        PAYMENTS = 'payments', 'Payments'
        QUOTATIONS = 'quotations', 'Quotations'
        PROJECTS = 'projects', 'Projects'
        INVOICING = 'invoicing', 'Invoicing'
        SUPPORT = 'support', 'Support'
        GLOBAL = 'global', 'Global'

    class Type(models.TextChoices):
        EMAIL = 'email', 'Email'
        WEBSOCKET = 'websocket', 'WebSocket'
        BOTH = 'both', 'Email y WebSocket'

    name = models.CharField(max_length=100)
    module = models.CharField(max_length=20, choices=Module.choices)
    notification_type = models.CharField(max_length=20, choices=Type.choices, default=Type.BOTH)
    subject = models.CharField(max_length=200)
    message_template = models.TextField()
    is_active = models.BooleanField(default=True)
    
    # Variables disponibles en la plantilla
    available_variables = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = "Notification Template"
        verbose_name_plural = "Notification Templates"
        db_table = 'notifications_template'
        unique_together = ['name', 'module']

    def __str__(self):
        return f"{self.module} - {self.name}"


class Notification(BaseModel):
    """
    Notificaciones enviadas a usuarios
    """
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendiente'
        SENT = 'sent', 'Enviada'
        FAILED = 'failed', 'Fallida'
        READ = 'read', 'Leída'

    class Priority(models.TextChoices):
        LOW = 'low', 'Baja'
        MEDIUM = 'medium', 'Media'
        HIGH = 'high', 'Alta'
        URGENT = 'urgent', 'Urgente'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    template = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    
    # Datos relacionados para contexto
    related_model = models.CharField(max_length=50, blank=True)
    related_id = models.IntegerField(null=True, blank=True)
    
    # Campos para seguimiento
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Datos adicionales
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        db_table = 'notifications_notification'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.user.email}"


class NotificationPreference(BaseModel):
    """
    Preferencias de notificación por usuario y módulo
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )
    module = models.CharField(max_length=20, choices=NotificationTemplate.Module.choices)
    
    # Tipos de notificación habilitados
    email_enabled = models.BooleanField(default=True)
    websocket_enabled = models.BooleanField(default=True)
    
    # Configuraciones específicas por módulo
    settings = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = "Notification Preference"
        verbose_name_plural = "Notification Preferences"
        db_table = 'notifications_preference'
        unique_together = ['user', 'module']

    def __str__(self):
        return f"{self.user.email} - {self.module}"


class NotificationLog(BaseModel):
    """
    Log de notificaciones enviadas para auditoría
    """
    class Channel(models.TextChoices):
        EMAIL = 'email', 'Email'
        WEBSOCKET = 'websocket', 'WebSocket'
        SMS = 'sms', 'SMS'

    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    channel = models.CharField(max_length=20, choices=Channel.choices)
    status = models.CharField(max_length=20, choices=Notification.Status.choices)
    sent_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True)
    
    # Datos de entrega
    delivery_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = "Notification Log"
        verbose_name_plural = "Notification Logs"
        db_table = 'notifications_log'
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.notification.subject} - {self.channel} - {self.status}" 