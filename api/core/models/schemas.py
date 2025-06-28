"""
Esquemas Dinámicos y Reutilizables para SmartHydro
Optimiza la gestión de variables y configuraciones
"""
from django.db import models
from django.core.cache import cache
from .utils import ModelApi
from .catchment_points import CatchmentPoint


class SchemaTemplate(ModelApi):
    """
    Plantilla de esquema reutilizable
    Define configuraciones estándar para diferentes tipos de pozos
    """
    name = models.CharField(max_length=200, verbose_name='Nombre del esquema')
    description = models.TextField(verbose_name='Descripción')
    category = models.CharField(max_length=100, verbose_name='Categoría')
    
    # Configuración física del pozo
    well_depth = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name='Profundidad del pozo (m)')
    pump_position = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name='Posición de la bomba (m)')
    level_sensor_position = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name='Posición del sensor de nivel (m)')
    pump_outlet_diameter = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name='Diámetro ducto salida bomba (pulg)')
    flowmeter_diameter = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name='Diámetro flujómetro (pulg)')
    initial_flowmeter_reading = models.IntegerField(
        default=0, verbose_name='Lectura inicial del caudalímetro')
    
    # Configuración de telemetría
    is_telemetry_enabled = models.BooleanField(
        default=False, verbose_name='Telemetría habilitada')
    default_frequency = models.CharField(
        max_length=10, default='60', verbose_name='Frecuencia por defecto (minutos)')
    
    # Proveedores soportados
    supported_providers = models.JSONField(
        default=list, verbose_name='Proveedores soportados')
    
    # Variables del esquema
    variables_config = models.JSONField(
        default=dict, verbose_name='Configuración de variables')
    
    # Configuración DGA
    dga_config = models.JSONField(
        default=dict, verbose_name='Configuración DGA')
    
    # Metadata
    version = models.CharField(max_length=20, default='1.0', verbose_name='Versión')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    is_public = models.BooleanField(default=False, verbose_name='Público')
    
    class Meta:
        verbose_name = 'Plantilla de Esquema'
        verbose_name_plural = 'Plantillas de Esquemas'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} v{self.version}"
    
    def get_cache_key(self):
        """Clave para cache del esquema"""
        return f"schema_template_{self.id}_{self.version}"
    
    def save(self, *args, **kwargs):
        """Invalidar cache al guardar"""
        super().save(*args, **kwargs)
        cache.delete(self.get_cache_key())
    
    def get_variables_config(self):
        """Obtener configuración de variables desde cache"""
        cache_key = self.get_cache_key()
        cached_config = cache.get(cache_key)
        
        if cached_config is None:
            cached_config = self.variables_config
            cache.set(cache_key, cached_config, timeout=3600)  # 1 hora
        
        return cached_config


class DynamicSchema(ModelApi):
    """
    Esquema dinámico aplicado a un punto de captación
    Hereda configuración de SchemaTemplate pero permite personalización
    """
    point = models.OneToOneField(
        CatchmentPoint, 
        on_delete=models.CASCADE, 
        related_name='dynamic_schema',
        verbose_name='Punto de captación'
    )
    
    template = models.ForeignKey(
        SchemaTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Plantilla base'
    )
    
    # Configuración personalizada (sobrescribe template)
    custom_config = models.JSONField(
        default=dict, verbose_name='Configuración personalizada')
    
    # Estado de telemetría
    is_telemetry_active = models.BooleanField(
        default=False, verbose_name='Telemetría activa')
    telemetry_start_date = models.DateField(
        null=True, blank=True, verbose_name='Fecha inicio telemetría')
    
    # Proveedor activo
    active_provider = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Proveedor activo')
    
    # Frecuencia de recolección
    collection_frequency = models.CharField(
        max_length=10, default='60', verbose_name='Frecuencia (minutos)')
    
    # Configuración de variables personalizada
    variables_override = models.JSONField(
        default=dict, verbose_name='Sobrescritura de variables')
    
    # Configuración DGA personalizada
    dga_override = models.JSONField(
        default=dict, verbose_name='Sobrescritura DGA')
    
    # Metadata
    last_config_update = models.DateTimeField(
        auto_now=True, verbose_name='Última actualización')
    config_version = models.CharField(
        max_length=20, default='1.0', verbose_name='Versión de configuración')
    
    class Meta:
        verbose_name = 'Esquema Dinámico'
        verbose_name_plural = 'Esquemas Dinámicos'
    
    def __str__(self):
        return f"Esquema de {self.point.title}"
    
    def get_cache_key(self):
        """Clave para cache del esquema dinámico"""
        return f"dynamic_schema_{self.point.id}_{self.config_version}"
    
    def save(self, *args, **kwargs):
        """Invalidar cache al guardar"""
        super().save(*args, **kwargs)
        cache.delete(self.get_cache_key())
        # Invalidar cache de puntos activos
        cache.delete('active_telemetry_points')
    
    def get_merged_config(self):
        """
        Obtener configuración fusionada (template + personalizada)
        """
        cache_key = self.get_cache_key()
        cached_config = cache.get(cache_key)
        
        if cached_config is None:
            # Configuración base del template
            base_config = self.template.get_variables_config() if self.template else {}
            
            # Fusionar con configuración personalizada
            merged_config = self._deep_merge(base_config, self.custom_config)
            
            # Aplicar sobrescrituras de variables
            if self.variables_override:
                merged_config = self._deep_merge(merged_config, self.variables_override)
            
            cache.set(cache_key, merged_config, timeout=1800)  # 30 minutos
            cached_config = merged_config
        
        return cached_config
    
    def get_dga_config(self):
        """Obtener configuración DGA fusionada"""
        base_dga = self.template.dga_config if self.template else {}
        return self._deep_merge(base_dga, self.dga_override)
    
    def _deep_merge(self, base, override):
        """Fusión profunda de diccionarios"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    def is_ready_for_telemetry(self):
        """Verificar si el esquema está listo para telemetría"""
        if not self.is_telemetry_active:
            return False
        
        config = self.get_merged_config()
        if not config.get('variables'):
            return False
        
        if not self.active_provider:
            return False
        
        return True


class VariableDefinition(ModelApi):
    """
    Definición de variable reutilizable
    Define cómo procesar una variable específica
    """
    name = models.CharField(max_length=100, verbose_name='Nombre de la variable')
    label = models.CharField(max_length=200, verbose_name='Etiqueta')
    description = models.TextField(verbose_name='Descripción')
    
    # Tipo de variable
    VARIABLE_TYPES = [
        ('LEVEL', 'Nivel'),
        ('FLOW', 'Caudal'),
        ('TOTAL', 'Totalizador'),
        ('TEMPERATURE', 'Temperatura'),
        ('PRESSURE', 'Presión'),
        ('PULSES', 'Pulsos'),
        ('CUSTOM', 'Personalizada'),
    ]
    
    variable_type = models.CharField(
        max_length=20, choices=VARIABLE_TYPES, verbose_name='Tipo de variable')
    
    # Configuración de procesamiento
    processing_config = models.JSONField(
        default=dict, verbose_name='Configuración de procesamiento')
    
    # Unidades
    unit = models.CharField(max_length=20, verbose_name='Unidad')
    unit_symbol = models.CharField(max_length=10, verbose_name='Símbolo de unidad')
    
    # Rangos válidos
    min_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Valor mínimo')
    max_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Valor máximo')
    
    # Configuración de validación
    validation_rules = models.JSONField(
        default=dict, verbose_name='Reglas de validación')
    
    # Metadata
    is_active = models.BooleanField(default=True, verbose_name='Activa')
    version = models.CharField(max_length=20, default='1.0', verbose_name='Versión')
    
    class Meta:
        verbose_name = 'Definición de Variable'
        verbose_name_plural = 'Definiciones de Variables'
        unique_together = ['name', 'version']
    
    def __str__(self):
        return f"{self.name} ({self.variable_type})"
    
    def get_processing_config(self):
        """Obtener configuración de procesamiento"""
        return self.processing_config
    
    def validate_value(self, value):
        """Validar valor según reglas"""
        if self.min_value is not None and value < self.min_value:
            return False, f"Valor menor al mínimo: {self.min_value}"
        
        if self.max_value is not None and value > self.max_value:
            return False, f"Valor mayor al máximo: {self.max_value}"
        
        # Validaciones personalizadas
        for rule in self.validation_rules.get('custom', []):
            if not self._apply_validation_rule(rule, value):
                return False, rule.get('message', 'Validación fallida')
        
        return True, "OK"


class ProviderConfiguration(ModelApi):
    """
    Configuración específica por proveedor
    Define cómo conectar y procesar datos de cada proveedor
    """
    name = models.CharField(max_length=100, verbose_name='Nombre del proveedor')
    provider_type = models.CharField(max_length=50, verbose_name='Tipo de proveedor')
    
    # Configuración de conexión
    connection_config = models.JSONField(
        default=dict, verbose_name='Configuración de conexión')
    
    # Configuración de autenticación
    auth_config = models.JSONField(
        default=dict, verbose_name='Configuración de autenticación')
    
    # Mapeo de variables
    variable_mapping = models.JSONField(
        default=dict, verbose_name='Mapeo de variables')
    
    # Configuración de procesamiento
    processing_config = models.JSONField(
        default=dict, verbose_name='Configuración de procesamiento')
    
    # Configuración de errores y reintentos
    error_config = models.JSONField(
        default=dict, verbose_name='Configuración de errores')
    
    # Estado
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    is_testing = models.BooleanField(default=False, verbose_name='En pruebas')
    
    class Meta:
        verbose_name = 'Configuración de Proveedor'
        verbose_name_plural = 'Configuraciones de Proveedores'
    
    def __str__(self):
        return f"{self.name} ({self.provider_type})"
    
    def get_cache_key(self):
        """Clave para cache del proveedor"""
        return f"provider_config_{self.name}_{self.provider_type}"
    
    def save(self, *args, **kwargs):
        """Invalidar cache al guardar"""
        super().save(*args, **kwargs)
        cache.delete(self.get_cache_key())


# Funciones de utilidad para optimizar consultas
def get_active_telemetry_points():
    """
    Obtener puntos con telemetría activa (cacheado)
    """
    cache_key = 'active_telemetry_points'
    cached_points = cache.get(cache_key)
    
    if cached_points is None:
        # Consulta optimizada
        active_points = DynamicSchema.objects.filter(
            is_telemetry_active=True
        ).select_related(
            'point', 'template'
        ).prefetch_related(
            'point__project__client'
        )
        
        cached_points = list(active_points)
        cache.set(cache_key, cached_points, timeout=300)  # 5 minutos
    
    return cached_points


def get_points_by_frequency(frequency):
    """
    Obtener puntos por frecuencia específica
    """
    cache_key = f'points_frequency_{frequency}'
    cached_points = cache.get(cache_key)
    
    if cached_points is None:
        points = DynamicSchema.objects.filter(
            is_telemetry_active=True,
            collection_frequency=frequency
        ).select_related('point', 'template')
        
        cached_points = list(points)
        cache.set(cache_key, cached_points, timeout=300)  # 5 minutos
    
    return cached_points


def get_points_by_provider(provider):
    """
    Obtener puntos por proveedor específico
    """
    cache_key = f'points_provider_{provider}'
    cached_points = cache.get(cache_key)
    
    if cached_points is None:
        points = DynamicSchema.objects.filter(
            is_telemetry_active=True,
            active_provider=provider
        ).select_related('point', 'template')
        
        cached_points = list(points)
        cache.set(cache_key, cached_points, timeout=300)  # 5 minutos
    
    return cached_points


def invalidate_telemetry_cache():
    """
    Invalidar todos los caches relacionados con telemetría
    """
    cache_keys = [
        'active_telemetry_points',
        'points_frequency_1',
        'points_frequency_5', 
        'points_frequency_60',
        'points_provider_twin',
        'points_provider_nettra',
        'points_provider_novus'
    ]
    
    for key in cache_keys:
        cache.delete(key) 