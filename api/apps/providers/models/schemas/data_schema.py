"""
Modelo de Esquema de Datos
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from api.apps.core.models import BaseModel


class DataSchema(BaseModel):
    """Esquemas de datos para diferentes tipos de variables"""
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Nombre del esquema')
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_('Descripción')
    )
    
    # Definición del esquema
    schema_definition = models.JSONField(
        verbose_name=_('Definición del esquema'),
        help_text=_('Definición JSON del esquema de datos')
    )
    
    # Variables que maneja este esquema
    supported_variables = models.JSONField(
        default=list,
        verbose_name=_('Variables soportadas'),
        help_text=_('Lista de variables que maneja este esquema')
    )
    
    # Configuración de procesamiento
    processing_rules = models.JSONField(
        default=dict,
        verbose_name=_('Reglas de procesamiento'),
        help_text=_('Reglas específicas de procesamiento para este esquema')
    )
    
    # Validaciones
    validation_rules = models.JSONField(
        default=dict,
        verbose_name=_('Reglas de validación'),
        help_text=_('Reglas de validación para los datos')
    )
    
    # Estado - is_active heredado de BaseModel
    # Metadata - created_at, updated_at heredados de BaseModel
    
    class Meta:
        verbose_name = _('Esquema de Datos')
        verbose_name_plural = _('Esquemas de Datos')
        db_table = 'providers_data_schema'
    
    def __str__(self):
        return self.name 