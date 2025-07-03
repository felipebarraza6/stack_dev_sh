"""
Modelo de Notificaciones de Puntos de Captación
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from api.apps.core.models import BaseModel
from ..points.catchment_point import CatchmentPoint


class NotificationsCatchment(BaseModel):
    """Notificaciones de puntos de captación"""
    
    NOTIFICATION_TYPES = [
        ('INFO', 'Informativo'),
        ('WARNING', 'Advertencia'),
        ('ALERT', 'Alerta'),
        ('CRITICAL', 'Crítico'),
        ('SUPPORT', 'Soporte'),
    ]
    
    point_catchment = models.ForeignKey(
        CatchmentPoint,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('Punto de captación')
    )
    
    type_variable = models.CharField(
        max_length=50,
        verbose_name=_('Tipo de variable')
    )
    
    type_notification = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        verbose_name=_('Tipo de notificación')
    )
    
    message = models.TextField(
        verbose_name=_('Mensaje')
    )
    
    # Estado - heredado de BaseModel
    # is_active, created_at, updated_at ya están en BaseModel
    
    class Meta:
        verbose_name = _('Notificación de Punto de Captación')
        verbose_name_plural = _('Notificaciones de Puntos de Captación')
        db_table = 'catchment_notifications_catchment'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.point_catchment.name} - {self.get_type_notification_display()}" 