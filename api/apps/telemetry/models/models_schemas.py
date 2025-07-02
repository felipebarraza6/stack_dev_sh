"""
Modelos de Esquemas de Telemetría
Sistema dinámico basado en esquemas para agrupación de datos
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
        return f"{self.name} ({self.get_schema_type_display()})"
    
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


class TelemetryGroup(models.Model):
    """Datos agrupados según esquemas de telemetría"""
    
    # Esquema aplicado
    schema = models.ForeignKey(
        TelemetrySchema,
        on_delete=models.CASCADE,
        related_name='groups',
        verbose_name=_('Esquema')
    )
    
    # Punto de captación
    catchment_point = models.ForeignKey(
        'catchment.CatchmentPoint',
        on_delete=models.CASCADE,
        related_name='telemetry_groups',
        verbose_name=_('Punto de captación')
    )
    
    # Timestamp de agrupación
    timestamp = models.DateTimeField(
        verbose_name=_('Timestamp de agrupación')
    )
    
    # Datos agrupados según esquema
    grouped_data = models.JSONField(
        verbose_name=_('Datos agrupados'),
        help_text=_('Datos agrupados según el esquema de telemetría')
    )
    
    # Campos calculados
    calculated_fields = models.JSONField(
        default=dict,
        verbose_name=_('Campos calculados'),
        help_text=_('Campos calculados según el esquema')
    )
    
    # Metadata de agrupación
    grouping_metadata = models.JSONField(
        default=dict,
        verbose_name=_('Metadata de agrupación'),
        help_text=_('Información sobre cómo se realizó la agrupación')
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
        verbose_name = _('Grupo de Telemetría')
        verbose_name_plural = _('Grupos de Telemetría')
        db_table = 'telemetry_telemetry_group'
        indexes = [
            models.Index(fields=['schema', 'catchment_point', 'timestamp']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['processing_status']),
        ]
        ordering = ['-timestamp']
        unique_together = ['schema', 'catchment_point', 'timestamp']
    
    def __str__(self):
        return f"{self.schema.name} - {self.catchment_point.name} - {self.timestamp}"
    
    def get_data_for_variable(self, variable_code):
        """Obtener datos para una variable específica"""
        return self.grouped_data.get(variable_code, {})
    
    def get_calculated_field(self, field_name):
        """Obtener un campo calculado específico"""
        return self.calculated_fields.get(field_name)


class TelemetrySchemaMapping(models.Model):
    """Mapeo entre esquemas y puntos de captación"""
    
    schema = models.ForeignKey(
        TelemetrySchema,
        on_delete=models.CASCADE,
        related_name='point_mappings',
        verbose_name=_('Esquema')
    )
    
    catchment_point = models.ForeignKey(
        'catchment.CatchmentPoint',
        on_delete=models.CASCADE,
        related_name='schema_mappings',
        verbose_name=_('Punto de captación')
    )
    
    # Configuración específica del mapeo
    mapping_config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración de mapeo'),
        help_text=_('Configuración específica para este punto y esquema')
    )
    
    # Variables específicas para este punto
    point_variables = models.ManyToManyField(
        'variables.Variable',
        blank=True,
        related_name='point_schema_mappings',
        verbose_name=_('Variables del punto')
    )
    
    # Transformaciones específicas
    transformations = models.JSONField(
        default=dict,
        verbose_name=_('Transformaciones'),
        help_text=_('Transformaciones específicas para este punto')
    )
    
    # Prioridad del mapeo
    priority = models.IntegerField(
        default=1,
        verbose_name=_('Prioridad'),
        help_text=_('Prioridad del mapeo (menor número = mayor prioridad)')
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
        verbose_name = _('Mapeo Esquema-Punto')
        verbose_name_plural = _('Mapeos Esquema-Punto')
        db_table = 'telemetry_telemetry_schema_mapping'
        unique_together = ['schema', 'catchment_point']
        ordering = ['priority']
    
    def __str__(self):
        return f"{self.schema.name} - {self.catchment_point.name}"


class TelemetrySchemaProcessor(models.Model):
    """Procesador de esquemas de telemetría"""
    
    PROCESSOR_TYPES = [
        ('AGGREGATION', 'Agregación'),
        ('CALCULATION', 'Cálculo'),
        ('VALIDATION', 'Validación'),
        ('TRANSFORMATION', 'Transformación'),
        ('CUSTOM', 'Personalizado'),
    ]
    
    name = models.CharField(
        max_length=100,
        verbose_name=_('Nombre del procesador')
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_('Descripción')
    )
    
    processor_type = models.CharField(
        max_length=20,
        choices=PROCESSOR_TYPES,
        verbose_name=_('Tipo de procesador')
    )
    
    # Esquemas a los que aplica
    schemas = models.ManyToManyField(
        TelemetrySchema,
        related_name='processors',
        verbose_name=_('Esquemas')
    )
    
    # Configuración del procesador
    processor_config = models.JSONField(
        verbose_name=_('Configuración del procesador'),
        help_text=_('Configuración específica del procesador')
    )
    
    # Código del procesador (Python)
    processor_code = models.TextField(
        blank=True,
        verbose_name=_('Código del procesador'),
        help_text=_('Código Python del procesador personalizado')
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
        verbose_name = _('Procesador de Esquema')
        verbose_name_plural = _('Procesadores de Esquemas')
        db_table = 'telemetry_telemetry_schema_processor'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_processor_type_display()})" 