"""
Modelo de Datos de Cumplimiento
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from ..configs.compliance_config import ComplianceConfig


class ComplianceData(models.Model):
    """Datos de cumplimiento enviados"""
    
    compliance_config = models.ForeignKey(
        ComplianceConfig,
        on_delete=models.CASCADE,
        related_name='data_sent',
        verbose_name=_('Configuración de cumplimiento')
    )
    
    # Datos enviados
    data = models.JSONField(
        verbose_name=_('Datos enviados'),
        help_text=_('Datos enviados a la fuente de cumplimiento')
    )
    
    # Estado del envío
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pendiente'),
            ('SENT', 'Enviado'),
            ('CONFIRMED', 'Confirmado'),
            ('REJECTED', 'Rechazado'),
            ('ERROR', 'Error'),
        ],
        default='PENDING',
        verbose_name=_('Estado')
    )
    
    # Respuesta de la fuente
    response = models.JSONField(
        default=dict,
        verbose_name=_('Respuesta'),
        help_text=_('Respuesta de la fuente de cumplimiento')
    )
    
    # Metadata
    sent_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Confirmado el')
    )
    
    class Meta:
        verbose_name = _('Dato de Cumplimiento')
        verbose_name_plural = _('Datos de Cumplimiento')
        db_table = 'compliance_compliance_data'
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.compliance_config} - {self.sent_at}" 