"""
Modelo de Fuente de Cumplimiento
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class ComplianceSource(models.Model):
    """Fuente de cumplimiento (DGA, SMA, etc.)"""
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Nombre de la fuente')
    )
    
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_('Código de la fuente')
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_('Descripción')
    )
    
    # Configuración de la fuente
    config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración'),
        help_text=_('Configuración específica de la fuente de cumplimiento')
    )
    
    # Variables que maneja esta fuente
    supported_variables = models.JSONField(
        default=list,
        verbose_name=_('Variables soportadas'),
        help_text=_('Lista de variables que maneja esta fuente')
    )
    
    # Estado
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Activa')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Fuente de Cumplimiento')
        verbose_name_plural = _('Fuentes de Cumplimiento')
        db_table = 'compliance_compliance_source'
    
    def __str__(self):
        return f"{self.name} ({self.code})" 