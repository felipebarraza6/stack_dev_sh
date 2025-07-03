"""
Modelo de Provider
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Provider(models.Model):
    """Proveedor de datos de telemetría"""
    
    PROVIDER_TYPES = [
        ('HTTP_API', 'HTTP API'),
        ('MQTT', 'MQTT Broker'),
        ('WEBSOCKET', 'WebSocket'),
        ('GRPC', 'gRPC'),
        ('CUSTOM', 'Custom Protocol'),
    ]
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Nombre del proveedor')
    )
    
    provider_type = models.CharField(
        max_length=20,
        choices=PROVIDER_TYPES,
        verbose_name=_('Tipo de proveedor')
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_('Descripción')
    )
    
    # Configuración de conexión
    connection_config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración de conexión'),
        help_text=_('Configuración específica del proveedor (URLs, credenciales, etc.)')
    )
    
    # Configuración de autenticación
    auth_config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración de autenticación'),
        help_text=_('Configuración de autenticación (tokens, API keys, etc.)')
    )
    
    # Configuración de procesamiento
    processing_config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración de procesamiento'),
        help_text=_('Configuración de procesamiento de datos')
    )
    
    # Estado del proveedor
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Activo')
    )
    
    is_testing = models.BooleanField(
        default=False,
        verbose_name=_('Modo testing')
    )
    
    # Métricas
    last_connection = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Última conexión')
    )
    
    connection_status = models.CharField(
        max_length=20,
        default='UNKNOWN',
        choices=[
            ('ONLINE', 'En línea'),
            ('OFFLINE', 'Desconectado'),
            ('ERROR', 'Error'),
            ('UNKNOWN', 'Desconocido'),
        ],
        verbose_name=_('Estado de conexión')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Proveedor')
        verbose_name_plural = _('Proveedores')
        db_table = 'providers_provider'
    
    def __str__(self):
        return self.name


class ProviderSchemaMapping(models.Model):
    """Mapeo entre proveedores y esquemas de datos"""
    
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name='schema_mappings',
        verbose_name=_('Proveedor')
    )
    
    schema = models.ForeignKey(
        'providers.DataSchema',
        on_delete=models.CASCADE,
        related_name='provider_mappings',
        verbose_name=_('Esquema de datos')
    )
    
    # Configuración específica del mapeo
    mapping_config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración de mapeo'),
        help_text=_('Configuración específica para este proveedor y esquema')
    )
    
    # Transformaciones de datos
    data_transformations = models.JSONField(
        default=dict,
        verbose_name=_('Transformaciones de datos'),
        help_text=_('Transformaciones específicas para los datos de este proveedor')
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
        verbose_name = _('Mapeo Proveedor-Esquema')
        verbose_name_plural = _('Mapeos Proveedor-Esquema')
        db_table = 'providers_provider_schema_mapping'
        unique_together = ['provider', 'schema']
        ordering = ['priority']
    
    def __str__(self):
        return f"{self.provider.name} - {self.schema.name}" 