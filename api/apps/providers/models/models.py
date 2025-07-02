"""
Modelos de Proveedores Dinámicos
Sistema flexible para múltiples proveedores incluyendo MQTT
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


class MQTTBroker(models.Model):
    """Configuración específica para brokers MQTT"""
    
    provider = models.OneToOneField(
        Provider,
        on_delete=models.CASCADE,
        related_name='mqtt_config',
        verbose_name=_('Proveedor')
    )
    
    # Configuración del broker
    broker_host = models.CharField(
        max_length=255,
        verbose_name=_('Host del broker')
    )
    
    broker_port = models.IntegerField(
        default=1883,
        verbose_name=_('Puerto del broker')
    )
    
    use_tls = models.BooleanField(
        default=False,
        verbose_name=_('Usar TLS')
    )
    
    # Autenticación
    username = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Usuario')
    )
    
    password = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Contraseña')
    )
    
    # Configuración de conexión
    keepalive = models.IntegerField(
        default=60,
        verbose_name=_('Keepalive (segundos)')
    )
    
    reconnect_delay = models.IntegerField(
        default=5,
        verbose_name=_('Delay de reconexión (segundos)')
    )
    
    # Topics de configuración
    topic_prefix = models.CharField(
        max_length=100,
        default='telemetry/',
        verbose_name=_('Prefijo de topics')
    )
    
    topic_pattern = models.CharField(
        max_length=200,
        default='{device_id}/data',
        verbose_name=_('Patrón de topics'),
        help_text=_('Patrón para construir topics. Variables: {device_id}, {variable_type}')
    )
    
    # Configuración de QoS
    qos_level = models.IntegerField(
        default=1,
        choices=[
            (0, 'QoS 0 - At most once'),
            (1, 'QoS 1 - At least once'),
            (2, 'QoS 2 - Exactly once'),
        ],
        verbose_name=_('Nivel de QoS')
    )
    
    class Meta:
        verbose_name = _('Configuración MQTT')
        verbose_name_plural = _('Configuraciones MQTT')
        db_table = 'providers_mqtt_broker'
    
    def __str__(self):
        return f"MQTT: {self.provider.name}"


class DeviceToken(models.Model):
    """Tokens de dispositivos para autenticación dinámica"""
    
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name='device_tokens',
        verbose_name=_('Proveedor')
    )
    
    device_id = models.CharField(
        max_length=100,
        verbose_name=_('ID del dispositivo')
    )
    
    token = models.CharField(
        max_length=255,
        verbose_name=_('Token de autenticación')
    )
    
    token_type = models.CharField(
        max_length=50,
        default='API_KEY',
        choices=[
            ('API_KEY', 'API Key'),
            ('JWT', 'JWT Token'),
            ('OAUTH', 'OAuth Token'),
            ('CUSTOM', 'Token Personalizado'),
        ],
        verbose_name=_('Tipo de token')
    )
    
    # Configuración del token
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Expira el')
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Activo')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Último uso')
    )
    
    class Meta:
        verbose_name = _('Token de Dispositivo')
        verbose_name_plural = _('Tokens de Dispositivos')
        db_table = 'providers_device_token'
        unique_together = ['provider', 'device_id']
    
    def __str__(self):
        return f"{self.device_id} - {self.provider.name}"


class DataSchema(models.Model):
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
    
    # Estado
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Activo')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Esquema de Datos')
        verbose_name_plural = _('Esquemas de Datos')
        db_table = 'providers_data_schema'
    
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
        DataSchema,
        on_delete=models.CASCADE,
        related_name='provider_mappings',
        verbose_name=_('Esquema')
    )
    
    # Configuración específica del mapeo
    mapping_config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración de mapeo'),
        help_text=_('Configuración específica para mapear datos del proveedor al esquema')
    )
    
    # Transformaciones
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
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Activo')
    )
    
    class Meta:
        verbose_name = _('Mapeo Proveedor-Esquema')
        verbose_name_plural = _('Mapeos Proveedor-Esquema')
        db_table = 'providers_provider_schema_mapping'
        unique_together = ['provider', 'schema']
    
    def __str__(self):
        return f"{self.provider.name} -> {self.schema.name}"


class DataIngestionLog(models.Model):
    """Log de ingesta de datos para monitoreo"""
    
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name='ingestion_logs',
        verbose_name=_('Proveedor')
    )
    
    device_id = models.CharField(
        max_length=100,
        verbose_name=_('ID del dispositivo')
    )
    
    schema = models.ForeignKey(
        DataSchema,
        on_delete=models.CASCADE,
        related_name='ingestion_logs',
        verbose_name=_('Esquema')
    )
    
    # Estado de la ingesta
    status = models.CharField(
        max_length=20,
        choices=[
            ('SUCCESS', 'Exitoso'),
            ('ERROR', 'Error'),
            ('PARTIAL', 'Parcial'),
            ('SKIPPED', 'Omitido'),
        ],
        verbose_name=_('Estado')
    )
    
    # Datos procesados
    records_processed = models.IntegerField(
        default=0,
        verbose_name=_('Registros procesados')
    )
    
    records_failed = models.IntegerField(
        default=0,
        verbose_name=_('Registros fallidos')
    )
    
    # Información de error
    error_message = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Mensaje de error')
    )
    
    # Metadata
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Completado el')
    )
    
    processing_time = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Tiempo de procesamiento (segundos)')
    )
    
    class Meta:
        verbose_name = _('Log de Ingesta')
        verbose_name_plural = _('Logs de Ingesta')
        db_table = 'providers_data_ingestion_log'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.provider.name} - {self.device_id} - {self.status}" 