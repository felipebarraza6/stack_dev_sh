"""
Modelo de Alerta para Variables
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from api.apps.core.models import BaseModel
from ..variables.variable import Variable


class VariableAlert(BaseModel):
    """Alertas para variables"""
    
    ALERT_TYPES = [
        ('THRESHOLD', 'Umbral'),
        ('TREND', 'Tendencia'),
        ('ANOMALY', 'Anomalía'),
        ('CUSTOM', 'Personalizada'),
    ]
    
    SEVERITY_LEVELS = [
        ('LOW', 'Baja'),
        ('MEDIUM', 'Media'),
        ('HIGH', 'Alta'),
        ('CRITICAL', 'Crítica'),
    ]
    
    name = models.CharField(
        max_length=100,
        verbose_name=_('Nombre de la alerta')
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_('Descripción')
    )
    
    variable = models.ForeignKey(
        Variable,
        on_delete=models.CASCADE,
        related_name='alerts',
        verbose_name=_('Variable')
    )
    
    alert_type = models.CharField(
        max_length=20,
        choices=ALERT_TYPES,
        verbose_name=_('Tipo de alerta')
    )
    
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_LEVELS,
        verbose_name=_('Severidad')
    )
    
    # Configuración de la alerta
    alert_config = models.JSONField(
        verbose_name=_('Configuración de alerta'),
        help_text=_('Configuración específica de la alerta')
    )
    
    # Condiciones de activación
    conditions = models.JSONField(
        verbose_name=_('Condiciones'),
        help_text=_('Condiciones que activan la alerta')
    )
    
    # Acciones a ejecutar
    actions = models.JSONField(
        default=list,
        verbose_name=_('Acciones'),
        help_text=_('Acciones a ejecutar cuando se activa la alerta')
    )
    
    # Estado - heredado de BaseModel
    # is_active, created_at, updated_at ya están en BaseModel
    
    class Meta:
        verbose_name = _('Alerta de Variable')
        verbose_name_plural = _('Alertas de Variables')
        db_table = 'variables_variable_alert'
        ordering = ['variable', 'severity', 'name']
    
    def __str__(self):
        return f"{self.variable.name} - {self.name} ({self.get_severity_display()})" 