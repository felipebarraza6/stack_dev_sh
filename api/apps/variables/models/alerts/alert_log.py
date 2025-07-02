"""
Modelo de Log de Alertas de Variables
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from .alert import VariableAlert
from ..data_points.data_point import VariableDataPoint


class VariableAlertLog(models.Model):
    """Log de alertas de variables"""
    
    alert = models.ForeignKey(
        VariableAlert,
        on_delete=models.CASCADE,
        related_name='alert_logs',
        verbose_name=_('Alerta')
    )
    
    data_point = models.ForeignKey(
        VariableDataPoint,
        on_delete=models.CASCADE,
        related_name='alert_logs',
        verbose_name=_('Punto de datos')
    )
    
    # Estado de la alerta
    status = models.CharField(
        max_length=20,
        choices=[
            ('TRIGGERED', 'Activada'),
            ('ACKNOWLEDGED', 'Reconocida'),
            ('RESOLVED', 'Resuelta'),
            ('CANCELLED', 'Cancelada'),
        ],
        verbose_name=_('Estado')
    )
    
    # Información del evento
    trigger_value = models.DecimalField(
        max_digits=15,
        decimal_places=6,
        verbose_name=_('Valor que activó la alerta')
    )
    
    threshold_value = models.DecimalField(
        max_digits=15,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name=_('Valor del umbral')
    )
    
    # Metadata
    triggered_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Reconocida el')
    )
    
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Resuelta el')
    )
    
    # Información adicional
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notas')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Log de Alerta')
        verbose_name_plural = _('Logs de Alertas')
        db_table = 'variables_variable_alert_log'
        ordering = ['-triggered_at']
    
    def __str__(self):
        return f"{self.alert.name} - {self.status} - {self.triggered_at}" 