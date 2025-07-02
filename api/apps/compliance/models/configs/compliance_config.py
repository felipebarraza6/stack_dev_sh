"""
Modelo de Configuración de Cumplimiento
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from ..sources.compliance_source import ComplianceSource


class ComplianceConfig(models.Model):
    """Configuración de cumplimiento para un punto de captación"""
    
    catchment_point = models.ForeignKey(
        'catchment.CatchmentPoint',
        on_delete=models.CASCADE,
        related_name='compliance_configs',
        verbose_name=_('Punto de captación')
    )
    
    compliance_source = models.ForeignKey(
        ComplianceSource,
        on_delete=models.CASCADE,
        related_name='configs',
        verbose_name=_('Fuente de cumplimiento')
    )
    
    # Configuración específica
    config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración específica'),
        help_text=_('Configuración específica para este punto y fuente')
    )
    
    # Estado
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Activo')
    )
    
    # Fechas de cumplimiento
    start_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Fecha de inicio')
    )
    
    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Fecha de fin')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Configuración de Cumplimiento')
        verbose_name_plural = _('Configuraciones de Cumplimiento')
        db_table = 'compliance_compliance_config'
        unique_together = ['catchment_point', 'compliance_source']
    
    def __str__(self):
        return f"{self.catchment_point.name} - {self.compliance_source.name}" 