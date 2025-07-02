"""
Modelo de Esquema de Variables
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class VariableSchema(models.Model):
    """Esquema de variables para diferentes tipos de datos"""
    
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
        help_text=_('Definición JSON del esquema de variables')
    )
    
    # Variables que incluye este esquema
    variables = models.JSONField(
        default=list,
        verbose_name=_('Variables del esquema'),
        help_text=_('Lista de variables que incluye este esquema')
    )
    
    # Configuración de procesamiento
    processing_config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración de procesamiento'),
        help_text=_('Configuración específica de procesamiento')
    )
    
    # Reglas de validación
    validation_rules = models.JSONField(
        default=dict,
        verbose_name=_('Reglas de validación'),
        help_text=_('Reglas de validación para las variables')
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
        verbose_name = _('Esquema de Variables')
        verbose_name_plural = _('Esquemas de Variables')
        db_table = 'variables_variable_schema'
    
    def __str__(self):
        return self.name 