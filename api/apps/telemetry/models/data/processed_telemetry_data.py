"""
Modelo de Datos Procesados de Telemetría
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from api.apps.telemetry.models.schemas.response_schema import ResponseSchema
from .raw_telemetry_data import RawTelemetryData


class ProcessedTelemetryData(models.Model):
    """Datos de telemetría procesados según esquemas"""
    
    # Punto de captación
    catchment_point = models.ForeignKey(
        'catchment.CatchmentPoint',
        on_delete=models.CASCADE,
        related_name='processed_telemetry_data',
        verbose_name=_('Punto de captación')
    )
    
    # Esquema aplicado
    response_schema = models.ForeignKey(
        ResponseSchema,
        on_delete=models.CASCADE,
        related_name='processed_data',
        verbose_name=_('Esquema de respuesta')
    )
    
    # Datos brutos originales
    raw_data = models.ForeignKey(
        RawTelemetryData,
        on_delete=models.CASCADE,
        related_name='processed_instances',
        verbose_name=_('Datos brutos originales')
    )
    
    # Timestamps
    measurement_time = models.DateTimeField(
        verbose_name=_('Fecha/hora medición')
    )
    
    # Datos procesados según esquema
    processed_data = models.JSONField(
        verbose_name=_('Datos procesados'),
        help_text=_('Datos procesados según el esquema de respuesta')
    )
    
    # Constantes aplicadas
    applied_constants = models.JSONField(
        default=list,
        verbose_name=_('Constantes aplicadas'),
        help_text=_('Lista de constantes aplicadas en el procesamiento')
    )
    
    # Estado de procesamiento
    processing_status = models.CharField(
        max_length=20,
        default='COMPLETED',
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
        verbose_name = _('Dato Procesado de Telemetría')
        verbose_name_plural = _('Datos Procesados de Telemetría')
        db_table = 'telemetry_processed_telemetry_data'
        indexes = [
            models.Index(fields=['catchment_point', 'measurement_time']),
            models.Index(fields=['response_schema', 'measurement_time']),
            models.Index(fields=['measurement_time']),
            models.Index(fields=['processing_status']),
        ]
        ordering = ['-measurement_time']
        unique_together = ['catchment_point', 'response_schema', 'measurement_time']
    
    def __str__(self):
        return f"{self.catchment_point.name} - {self.response_schema.name} - {self.measurement_time}" 