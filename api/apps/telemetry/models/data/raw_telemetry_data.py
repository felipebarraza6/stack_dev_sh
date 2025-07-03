"""
Modelo de Datos Brutos de Telemetría
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from api.apps.core.models import TimestampedModel


class RawTelemetryData(TimestampedModel):
    """Datos brutos de telemetría - almacenamiento sin procesar"""
    
    # Punto de captación
    catchment_point = models.ForeignKey(
        'catchment.CatchmentPoint',
        on_delete=models.CASCADE,
        related_name='raw_telemetry_data',
        verbose_name=_('Punto de captación')
    )
    
    # Timestamps - timestamp y device_timestamp heredados de TimestampedModel
    # measurement_time -> timestamp
    # logger_time -> device_timestamp
    
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
    
    # Metadata - created_at, updated_at heredados de TimestampedModel
    
    class Meta:
        verbose_name = _('Dato Bruto de Telemetría')
        verbose_name_plural = _('Datos Brutos de Telemetría')
        db_table = 'telemetry_raw_telemetry_data'
        indexes = [
            models.Index(fields=['catchment_point', 'timestamp']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['is_processed']),
            models.Index(fields=['processing_status']),
        ]
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.catchment_point.name} - {self.timestamp}" 