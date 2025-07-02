"""
Modelo de Esquema de Respuesta
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class ResponseSchema(models.Model):
    """Esquemas de respuesta configurables para API"""
    
    SCHEMA_TYPES = [
        ('MEASUREMENT', 'Mediciones'),
        ('PROCESSED', 'Datos procesados'),
        ('AGGREGATED', 'Datos agregados'),
        ('CUSTOM', 'Personalizado'),
    ]
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Nombre del esquema')
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_('Descripción')
    )
    
    schema_type = models.CharField(
        max_length=20,
        choices=SCHEMA_TYPES,
        verbose_name=_('Tipo de esquema')
    )
    
    # Definición del esquema
    schema_definition = models.JSONField(
        verbose_name=_('Definición del esquema'),
        help_text=_('Definición JSON del esquema de respuesta')
    )
    
    # Configuración de procesamiento
    processing_config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración de procesamiento'),
        help_text=_('Configuración específica de procesamiento')
    )
    
    # Variables que incluye este esquema
    included_variables = models.JSONField(
        default=list,
        verbose_name=_('Variables incluidas'),
        help_text=_('Lista de variables que incluye este esquema')
    )
    
    # Transformaciones específicas
    transformations = models.JSONField(
        default=dict,
        verbose_name=_('Transformaciones'),
        help_text=_('Transformaciones específicas para este esquema')
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
        verbose_name = _('Esquema de Respuesta')
        verbose_name_plural = _('Esquemas de Respuesta')
        db_table = 'telemetry_response_schema'
    
    def __str__(self):
        return f"{self.name} ({self.schema_type})" 