"""
Modelo de Datos Brutos de Telemetría
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class RawTelemetryData(models.Model):
    """Datos brutos de telemetría - almacenamiento sin procesar"""
    
    # Punto de captación
    catchment_point = models.ForeignKey(
        'catchment.CatchmentPoint',
        on_delete=models.CASCADE,
        related_name='raw_telemetry_data',
        verbose_name=_('Punto de captación')
    )
    
    # Timestamps
    measurement_time = models.DateTimeField(
        verbose_name=_('Fecha/hora medición')
    )
    
    logger_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Fecha/hora logger')
    )
    
    # Datos brutos - almacenamiento flexible
    raw_data = models.JSONField(
        verbose_name=_('Datos brutos'),
        help_text=_('Datos brutos recibidos del dispositivo')
    )
    
    # Estado de procesamiento
    is_processed = models.BooleanField(
        default=False,
        verbose_name=_('Procesado')
    )
    
    processing_status = models.CharField(
        max_length=20,
        default='PENDING',
        choices=[
            ('PENDING', 'Pendiente'),
            ('PROCESSING', 'Procesando'),
            ('COMPLETED', 'Completado'),
            ('FAILED', 'Fallido'),
            ('SKIPPED', 'Omitido'),
        ],
        verbose_name=_('Estado de procesamiento')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Dato Bruto de Telemetría')
        verbose_name_plural = _('Datos Brutos de Telemetría')
        db_table = 'telemetry_raw_telemetry_data'
        indexes = [
            models.Index(fields=['catchment_point', 'measurement_time']),
            models.Index(fields=['measurement_time']),
            models.Index(fields=['is_processed']),
            models.Index(fields=['processing_status']),
        ]
        ordering = ['-measurement_time']
    
    def __str__(self):
        return f"{self.catchment_point.name} - {self.measurement_time}" 