"""
Modelo de Mapeo entre Esquemas y Variables
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from .schema import VariableSchema
from ..variables.variable import Variable


class VariableSchemaMapping(models.Model):
    """Mapeo entre esquemas y variables"""
    
    schema = models.ForeignKey(
        VariableSchema,
        on_delete=models.CASCADE,
        related_name='variable_mappings',
        verbose_name=_('Esquema')
    )
    
    variable = models.ForeignKey(
        Variable,
        on_delete=models.CASCADE,
        related_name='schema_mappings',
        verbose_name=_('Variable')
    )
    
    mapping_config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración de mapeo'),
        help_text=_('Configuración específica para este mapeo')
    )
    
    # Transformaciones específicas
    transformations = models.JSONField(
        default=dict,
        verbose_name=_('Transformaciones'),
        help_text=_('Transformaciones específicas para esta variable en este esquema')
    )
    
    # Prioridad del mapeo
    priority = models.IntegerField(
        default=1,
        verbose_name=_('Prioridad'),
        help_text=_('Prioridad del mapeo (menor número = mayor prioridad)')
    )
    
    is_required = models.BooleanField(
        default=True,
        verbose_name=_('Requerida'),
        help_text=_('Indica si esta variable es requerida en el esquema')
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Activo')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Mapeo Esquema-Variable')
        verbose_name_plural = _('Mapeos Esquema-Variable')
        db_table = 'variables_variable_schema_mapping'
        unique_together = ['schema', 'variable']
        ordering = ['priority']
    
    def __str__(self):
        return f"{self.schema.name} - {self.variable.name}" 