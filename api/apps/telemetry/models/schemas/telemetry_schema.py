"""
Modelo de Esquema de Telemetría
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class TelemetrySchema(models.Model):
    """Esquema de agrupación para datos de telemetría"""
    
    SCHEMA_TYPES = [
        ('MEASUREMENT', 'Medición'),
        ('DASHBOARD', 'Dashboard'),
        ('REPORT', 'Reporte'),
        ('ALERT', 'Alerta'),
        ('COMPLIANCE', 'Cumplimiento'),
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
    
    # Variables que incluye este esquema
    variables = models.ManyToManyField(
        'variables.Variable',
        related_name='telemetry_schemas',
        verbose_name=_('Variables del esquema')
    )
    
    # Configuración de agrupación
    grouping_config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración de agrupación'),
        help_text=_('Configuración para agrupar datos (ventana de tiempo, agregación, etc.)')
    )
    
    # Configuración de visualización
    display_config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración de visualización'),
        help_text=_('Configuración para mostrar datos (gráficos, tablas, etc.)')
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
        help_text=_('Reglas de validación para los datos del esquema')
    )
    
    # Campos calculados
    calculated_fields = models.JSONField(
        default=list,
        verbose_name=_('Campos calculados'),
        help_text=_('Lista de campos calculados para este esquema')
    )
    
    # Estado
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Activo')
    )
    
    # Metadata
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_telemetry_schemas',
        verbose_name=_('Creado por')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Esquema de Telemetría')
        verbose_name_plural = _('Esquemas de Telemetría')
        db_table = 'telemetry_telemetry_schema'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.schema_type})"
    
    def get_variables_list(self):
        """Obtener lista de códigos de variables"""
        return list(self.variables.values_list('code', flat=True))
    
    def get_grouping_config(self):
        """Obtener configuración de agrupación con valores por defecto"""
        default_config = {
            'time_window': '1_hour',
            'aggregation': 'average',
            'group_by': ['catchment_point', 'variable'],
            'order_by': ['timestamp']
        }
        default_config.update(self.grouping_config)
        return default_config 