"""
Modelo unificado para almacenamiento de mediciones de telemetría
"""
from django.db import models
from django.contrib.postgres.indexes import GinIndex
from decimal import Decimal
import json

from api.apps.common.models import BaseModel
from .points import CatchmentPoint
from .schemes import Variable


class Measurement(BaseModel):
    """
    Modelo unificado para todas las mediciones de telemetría.
    
    Este modelo reemplaza a InteractionDetail y TimeSeriesData,
    proporcionando un almacenamiento eficiente y consistente
    para todos los tipos de datos de telemetría.
    """
    # Relaciones principales
    point = models.ForeignKey(
        CatchmentPoint, 
        on_delete=models.CASCADE,
        related_name='measurements',
        verbose_name='Punto de captación'
    )
    variable = models.ForeignKey(
        Variable,
        on_delete=models.CASCADE,
        related_name='measurements',
        verbose_name='Variable'
    )
    
    # Timestamp de la medición (indexado para consultas eficientes)
    timestamp = models.DateTimeField(
        db_index=True,
        verbose_name='Timestamp de medición'
    )
    
    # Valores procesados (optimizados para consultas)
    value_numeric = models.DecimalField(
        max_digits=15, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name='Valor numérico'
    )
    value_text = models.TextField(
        null=True, 
        blank=True,
        verbose_name='Valor de texto'
    )
    value_boolean = models.BooleanField(
        null=True, 
        blank=True,
        verbose_name='Valor booleano'
    )
    
    # Metadatos de la medición
    raw_value = models.JSONField(
        default=dict,
        help_text='Valor original del proveedor',
        verbose_name='Valor original'
    )
    quality_score = models.FloatField(
        default=1.0,
        help_text='Puntuación de calidad (0.0 - 1.0)',
        verbose_name='Puntuación de calidad'
    )
    provider = models.CharField(
        max_length=50,
        verbose_name='Proveedor'
    )
    
    # Configuración aplicada durante el procesamiento
    processing_config = models.JSONField(
        default=dict,
        help_text='Configuración aplicada durante el procesamiento',
        verbose_name='Configuración de procesamiento'
    )
    
    # Campos adicionales para compatibilidad
    days_since_last_connection = models.IntegerField(
        default=0,
        verbose_name='Días desde última conexión'
    )
    
    class Meta:
        verbose_name = "Medición"
        verbose_name_plural = "Mediciones"
        db_table = 'telemetry_measurement'
        ordering = ['-timestamp']
        
        # Índices optimizados para consultas frecuentes
        indexes = [
            # Consultas por punto y variable
            models.Index(fields=['point', 'variable', '-timestamp']),
            
            # Consultas por timestamp
            models.Index(fields=['timestamp']),
            
            # Consultas por proveedor
            models.Index(fields=['provider', '-timestamp']),
            
            # Consultas por variable
            models.Index(fields=['variable', '-timestamp']),
            
            # Índice GIN para búsquedas en JSON
            GinIndex(fields=['raw_value']),
            GinIndex(fields=['processing_config']),
        ]
        
        # Índices únicos para evitar duplicados
        unique_together = [
            ('point', 'variable', 'timestamp'),
        ]

    def __str__(self):
        return f"{self.point.name} - {self.variable.name} - {self.timestamp}"

    @property
    def value(self):
        """
        Obtener el valor principal de la medición
        """
        if self.value_numeric is not None:
            return float(self.value_numeric)
        elif self.value_text:
            return self.value_text
        elif self.value_boolean is not None:
            return self.value_boolean
        else:
            return self.raw_value

    @value.setter
    def value(self, val):
        """
        Establecer el valor principal de la medición
        """
        if isinstance(val, (int, float, Decimal)):
            self.value_numeric = Decimal(str(val))
            self.value_text = None
            self.value_boolean = None
        elif isinstance(val, bool):
            self.value_boolean = val
            self.value_numeric = None
            self.value_text = None
        elif isinstance(val, str):
            self.value_text = val
            self.value_numeric = None
            self.value_boolean = None
        else:
            # Para otros tipos, guardar en raw_value
            self.raw_value = val
            self.value_numeric = None
            self.value_text = None
            self.value_boolean = None

    def get_formatted_value(self, format_type='numeric'):
        """
        Obtener el valor formateado según el tipo especificado
        """
        if format_type == 'numeric':
            return float(self.value_numeric) if self.value_numeric else None
        elif format_type == 'text':
            return self.value_text
        elif format_type == 'boolean':
            return self.value_boolean
        elif format_type == 'raw':
            return self.raw_value
        else:
            return self.value

    def is_valid(self):
        """
        Verificar si la medición es válida
        """
        return (
            self.quality_score >= 0.5 and
            self.timestamp is not None and
            self.value is not None
        )

    def get_processing_summary(self):
        """
        Obtener resumen de la configuración de procesamiento aplicada
        """
        config = self.processing_config or {}
        return {
            'pulse_factor': config.get('pulse_factor'),
            'constant_addition': config.get('constant_addition'),
            'unit_conversion': config.get('unit_conversion'),
            'quality_filters': config.get('quality_filters'),
        }


class MeasurementBatch(BaseModel):
    """
    Lote de mediciones para procesamiento eficiente
    """
    batch_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='ID del lote'
    )
    provider = models.CharField(
        max_length=50,
        verbose_name='Proveedor'
    )
    frequency = models.CharField(
        max_length=10,
        verbose_name='Frecuencia'
    )
    total_measurements = models.IntegerField(
        default=0,
        verbose_name='Total de mediciones'
    )
    processed_measurements = models.IntegerField(
        default=0,
        verbose_name='Mediciones procesadas'
    )
    failed_measurements = models.IntegerField(
        default=0,
        verbose_name='Mediciones fallidas'
    )
    processing_time_ms = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Tiempo de procesamiento (ms)'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pendiente'),
            ('processing', 'Procesando'),
            ('completed', 'Completado'),
            ('failed', 'Fallido'),
        ],
        default='pending',
        verbose_name='Estado'
    )
    
    # Metadatos del lote
    metadata = models.JSONField(
        default=dict,
        verbose_name='Metadatos'
    )

    class Meta:
        verbose_name = "Lote de Mediciones"
        verbose_name_plural = "Lotes de Mediciones"
        db_table = 'telemetry_measurement_batch'
        ordering = ['-created_at']

    def __str__(self):
        return f"Batch {self.batch_id} - {self.provider} - {self.status}"

    @property
    def success_rate(self):
        """
        Calcular tasa de éxito del lote
        """
        if self.total_measurements == 0:
            return 0.0
        return (self.processed_measurements / self.total_measurements) * 100


class MeasurementQuality(BaseModel):
    """
    Métricas de calidad para mediciones
    """
    measurement = models.OneToOneField(
        Measurement,
        on_delete=models.CASCADE,
        related_name='quality_metrics',
        verbose_name='Medición'
    )
    
    # Métricas de calidad
    outlier_score = models.FloatField(
        default=0.0,
        help_text='Puntuación de outlier (0.0 - 1.0)',
        verbose_name='Puntuación de outlier'
    )
    consistency_score = models.FloatField(
        default=1.0,
        help_text='Puntuación de consistencia (0.0 - 1.0)',
        verbose_name='Puntuación de consistencia'
    )
    completeness_score = models.FloatField(
        default=1.0,
        help_text='Puntuación de completitud (0.0 - 1.0)',
        verbose_name='Puntuación de completitud'
    )
    
    # Flags de calidad
    is_outlier = models.BooleanField(
        default=False,
        verbose_name='Es outlier'
    )
    is_missing = models.BooleanField(
        default=False,
        verbose_name='Falta dato'
    )
    is_interpolated = models.BooleanField(
        default=False,
        verbose_name='Es interpolado'
    )
    
    # Comentarios de calidad
    quality_notes = models.TextField(
        blank=True,
        verbose_name='Notas de calidad'
    )

    class Meta:
        verbose_name = "Métrica de Calidad"
        verbose_name_plural = "Métricas de Calidad"
        db_table = 'telemetry_measurement_quality'

    def __str__(self):
        return f"Quality for {self.measurement}"

    @property
    def overall_quality_score(self):
        """
        Calcular puntuación de calidad general
        """
        scores = [
            self.outlier_score,
            self.consistency_score,
            self.completeness_score
        ]
        return sum(scores) / len(scores) 