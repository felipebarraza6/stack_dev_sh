"""
Modelo de Punto de Datos para Variables
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from ..variables.variable import Variable


class VariableDataPoint(models.Model):
    """Punto de datos para una variable específica"""
    
    variable = models.ForeignKey(
        Variable,
        on_delete=models.CASCADE,
        related_name='data_points',
        verbose_name=_('Variable')
    )
    
    # Identificación del punto de captación
    catchment_point_id = models.IntegerField(
        verbose_name=_('ID del punto de captación')
    )
    
    # Valor del dato
    value = models.DecimalField(
        max_digits=15,
        decimal_places=6,
        verbose_name=_('Valor')
    )
    
    # Timestamp del dato
    timestamp = models.DateTimeField(
        verbose_name=_('Timestamp')
    )
    
    # Calidad del dato
    quality = models.CharField(
        max_length=20,
        default='GOOD',
        choices=[
            ('GOOD', 'Bueno'),
            ('UNCERTAIN', 'Incierto'),
            ('BAD', 'Malo'),
            ('UNKNOWN', 'Desconocido'),
        ],
        verbose_name=_('Calidad del dato')
    )
    
    # Metadata adicional
    metadata = models.JSONField(
        default=dict,
        verbose_name=_('Metadata'),
        help_text=_('Información adicional del punto de datos')
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
        verbose_name = _('Punto de Datos')
        verbose_name_plural = _('Puntos de Datos')
        db_table = 'variables_variable_data_point'
        indexes = [
            models.Index(fields=['variable', 'catchment_point_id', 'timestamp']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['quality']),
            models.Index(fields=['processing_status']),
        ]
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.variable.name} - {self.timestamp} - {self.value}" 