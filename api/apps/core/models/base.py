"""
Modelos Base Abstractos
Proporciona modelos base reutilizables para toda la aplicación
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class BaseModel(models.Model):
    """
    Modelo base abstracto con campos comunes de auditoría
    """
    # Campos de auditoría
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Fecha de creación'),
        help_text=_('Fecha y hora de creación del registro')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Fecha de actualización'),
        help_text=_('Fecha y hora de la última actualización')
    )
    
    # Estado activo
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Activo'),
        help_text=_('Indica si el registro está activo')
    )
    
    class Meta:
        abstract = True
        ordering = ['-created_at']
    
    def __str__(self):
        """Representación por defecto usando el primer campo no abstracto"""
        for field in self._meta.fields:
            if not field.is_relation and field.name not in ['created_at', 'updated_at', 'is_active']:
                return str(getattr(self, field.name))
        return f"{self.__class__.__name__} #{self.pk}"
    
    @property
    def is_recent(self):
        """Verifica si el registro fue creado en las últimas 24 horas"""
        return (timezone.now() - self.created_at).days == 0
    
    @property
    def age_days(self):
        """Retorna la edad del registro en días"""
        return (timezone.now() - self.created_at).days


class TimestampedModel(BaseModel):
    """
    Modelo base con timestamps adicionales
    Extiende BaseModel con campos de timestamp específicos
    """
    # Timestamp de medición/evento
    timestamp = models.DateTimeField(
        verbose_name=_('Timestamp'),
        help_text=_('Fecha y hora del evento o medición')
    )
    
    # Timestamp del dispositivo/logger
    device_timestamp = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Timestamp del dispositivo'),
        help_text=_('Fecha y hora reportada por el dispositivo')
    )
    
    class Meta:
        abstract = True
        ordering = ['-timestamp']
    
    @property
    def time_difference(self):
        """Diferencia entre timestamp del dispositivo y timestamp del sistema"""
        if self.device_timestamp:
            return abs((self.timestamp - self.device_timestamp).total_seconds())
        return 0


class SoftDeleteModel(BaseModel):
    """
    Modelo base con soft delete
    Permite "eliminar" registros sin borrarlos físicamente
    """
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Fecha de eliminación'),
        help_text=_('Fecha y hora de eliminación (soft delete)')
    )
    
    deleted_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_deleted',
        verbose_name=_('Eliminado por'),
        help_text=_('Usuario que realizó la eliminación')
    )
    
    class Meta:
        abstract = True
    
    @property
    def is_deleted(self):
        """Verifica si el registro está marcado como eliminado"""
        return self.deleted_at is not None
    
    def soft_delete(self, user=None):
        """Marca el registro como eliminado sin borrarlo físicamente"""
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.is_active = False
        self.save(update_fields=['deleted_at', 'deleted_by', 'is_active'])
    
    def restore(self):
        """Restaura un registro eliminado"""
        self.deleted_at = None
        self.deleted_by = None
        self.is_active = True
        self.save(update_fields=['deleted_at', 'deleted_by', 'is_active'])
    
    def hard_delete(self):
        """Elimina físicamente el registro"""
        super().delete() 