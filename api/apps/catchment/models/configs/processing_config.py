"""
Modelo de Configuración de Procesamiento
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from ..points.catchment_point import CatchmentPoint


class CatchmentPointProcessingConfig(models.Model):
    """Configuración de procesamiento para un punto de captación"""
    
    catchment_point = models.OneToOneField(
        CatchmentPoint,
        on_delete=models.CASCADE,
        related_name='processing_config',
        verbose_name=_('Punto de captación')
    )
    
    # Configuración de posiciones
    pump_position = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Posición bomba (m)'),
        help_text=_('Posicionamiento de la bomba')
    )
    
    level_position = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Posición nivel (m)'),
        help_text=_('Posicionamiento del sensor de nivel')
    )
    
    depth = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Profundidad (m)'),
        help_text=_('Profundidad total del pozo')
    )
    
    pipe_diameter = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Diámetro ducto (pulg)'),
        help_text=_('Diámetro del ducto de salida de la bomba')
    )
    
    flowmeter_diameter = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Diámetro flujómetro (pulg)'),
        help_text=_('Diámetro del flujómetro')
    )
    
    # Configuración adicional
    additional_config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración adicional'),
        help_text=_('Configuración adicional específica del punto')
    )
    
    # Estado
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Activo')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Configuración de Procesamiento')
        verbose_name_plural = _('Configuraciones de Procesamiento')
        db_table = 'catchment_catchment_point_processing_config'
    
    def __str__(self):
        return f"Configuración de {self.catchment_point.name}"
    
    def calculate_water_table(self, measured_level):
        """Calcular nivel freático basado en la posición del sensor"""
        if measured_level is not None and self.level_position is not None:
            return float(measured_level) - float(self.level_position)
        return measured_level 