"""
Ejemplos de uso de modelos base
"""
from api.apps.core.models.base import BaseModel, TimestampedModel, SoftDeleteModel
from django.db import models
from django.utils.translation import gettext_lazy as _


# ============================================================================
# EJEMPLO 1: Modelo básico con BaseModel
# ============================================================================

class ExampleConfig(BaseModel):
    """Ejemplo de configuración usando BaseModel"""
    
    name = models.CharField(
        max_length=100,
        verbose_name=_('Nombre')
    )
    
    value = models.JSONField(
        verbose_name=_('Valor')
    )
    
    class Meta:
        verbose_name = _('Configuración de Ejemplo')
        verbose_name_plural = _('Configuraciones de Ejemplo')
        db_table = 'core_example_config'


# ============================================================================
# EJEMPLO 2: Modelo con timestamps usando TimestampedModel
# ============================================================================

class ExampleMeasurement(TimestampedModel):
    """Ejemplo de medición usando TimestampedModel"""
    
    sensor_id = models.CharField(
        max_length=50,
        verbose_name=_('ID del Sensor')
    )
    
    value = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name=_('Valor')
    )
    
    unit = models.CharField(
        max_length=20,
        verbose_name=_('Unidad')
    )
    
    class Meta:
        verbose_name = _('Medición de Ejemplo')
        verbose_name_plural = _('Mediciones de Ejemplo')
        db_table = 'core_example_measurement'
    
    def __str__(self):
        return f"{self.sensor_id}: {self.value} {self.unit}"


# ============================================================================
# EJEMPLO 3: Modelo con soft delete usando SoftDeleteModel
# ============================================================================

class ExampleDocument(SoftDeleteModel):
    """Ejemplo de documento usando SoftDeleteModel"""
    
    title = models.CharField(
        max_length=200,
        verbose_name=_('Título')
    )
    
    content = models.TextField(
        verbose_name=_('Contenido')
    )
    
    file_path = models.CharField(
        max_length=500,
        verbose_name=_('Ruta del archivo')
    )
    
    class Meta:
        verbose_name = _('Documento de Ejemplo')
        verbose_name_plural = _('Documentos de Ejemplo')
        db_table = 'core_example_document'
    
    def __str__(self):
        return self.title


# ============================================================================
# EJEMPLO 4: Modelo que combina múltiples características
# ============================================================================

class ExampleEvent(TimestampedModel, SoftDeleteModel):
    """Ejemplo de evento que combina timestamps y soft delete"""
    
    EVENT_TYPES = [
        ('INFO', 'Informativo'),
        ('WARNING', 'Advertencia'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Crítico'),
    ]
    
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        verbose_name=_('Tipo de evento')
    )
    
    message = models.TextField(
        verbose_name=_('Mensaje')
    )
    
    source = models.CharField(
        max_length=100,
        verbose_name=_('Fuente')
    )
    
    class Meta:
        verbose_name = _('Evento de Ejemplo')
        verbose_name_plural = _('Eventos de Ejemplo')
        db_table = 'core_example_event'
    
    def __str__(self):
        return f"{self.get_event_type_display()}: {self.message[:50]}" 