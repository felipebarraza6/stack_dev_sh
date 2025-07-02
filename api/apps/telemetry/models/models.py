"""
Modelos de Telemetría
Sistema moderno para gestión de datos de telemetría
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class TelemetryData(models.Model):
    """Datos de telemetría principales"""
    
    # Punto de captación
    catchment_point = models.ForeignKey(
        'catchment.CatchmentPoint',
        on_delete=models.CASCADE,
        related_name='telemetry_data',
        verbose_name=_('Punto de captación')
    )
    
    # Timestamps
    measurement_time = models.DateTimeField(
        verbose_name=_('Fecha/hora medición')
    )
    
    logger_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Fecha/hora logger')
    )
    
    # Datos principales
    flow = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name=_('Caudal (l/s)')
    )
    
    total = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name=_('Total (m³)')
    )
    
    total_diff = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        default=0,
        verbose_name=_('Consumo (m³/h)')
    )
    
    total_today_diff = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        default=0,
        verbose_name=_('Consumo hoy (m³)')
    )
    
    level = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name=_('Nivel (m)')
    )
    
    water_table = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name=_('Nivel freático (m)')
    )
    
    # Datos adicionales
    pulses = models.IntegerField(
        default=0,
        verbose_name=_('Pulsos')
    )
    
    days_not_connection = models.IntegerField(
        default=0,
        verbose_name=_('Días sin conexión')
    )
    
    # Estado de envío DGA
    send_dga = models.BooleanField(
        default=False,
        verbose_name=_('Enviado a DGA')
    )
    
    dga_response = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Respuesta DGA')
    )
    
    dga_voucher = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Voucher DGA')
    )
    
    # Estados
    is_warning = models.BooleanField(
        default=False,
        verbose_name=_('Alerta')
    )
    
    is_error = models.BooleanField(
        default=False,
        verbose_name=_('Error')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Dato de Telemetría')
        verbose_name_plural = _('Datos de Telemetría')
        db_table = 'telemetry_telemetry_data'
        indexes = [
            models.Index(fields=['catchment_point', 'measurement_time']),
            models.Index(fields=['measurement_time']),
            models.Index(fields=['send_dga']),
        ]
        ordering = ['-measurement_time']
    
    def __str__(self):
        return f"{self.catchment_point.name} - {self.measurement_time}"
    
    def calculate_water_table(self):
        """Calcular nivel freático basado en configuración del punto"""
        if self.level is not None:
            config = self.catchment_point.processing_config
            if config and config.level_position:
                return float(self.level) - float(config.level_position)
        return self.water_table


class TelemetryNotification(models.Model):
    """Notificaciones de telemetría"""
    
    NOTIFICATION_TYPES = [
        ('INFO', 'Informativo'),
        ('WARNING', 'Advertencia'),
        ('ALERT', 'Alerta'),
        ('CRITICAL', 'Crítico'),
        ('SUPPORT', 'Soporte'),
    ]
    
    catchment_point = models.ForeignKey(
        'catchment.CatchmentPoint',
        on_delete=models.CASCADE,
        related_name='telemetry_notifications',
        verbose_name=_('Punto de captación')
    )
    
    title = models.CharField(
        max_length=300,
        verbose_name=_('Título')
    )
    
    message = models.CharField(
        max_length=500,
        verbose_name=_('Mensaje')
    )
    
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        verbose_name=_('Tipo de notificación')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Notificación de Telemetría')
        verbose_name_plural = _('Notificaciones de Telemetría')
        db_table = 'telemetry_telemetry_notification'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.catchment_point.name} - {self.title}"


class TelemetryNotificationResponse(models.Model):
    """Respuestas a notificaciones de telemetría"""
    
    notification = models.ForeignKey(
        TelemetryNotification,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name=_('Notificación')
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='telemetry_notification_responses',
        verbose_name=_('Usuario')
    )
    
    response = models.CharField(
        max_length=300,
        verbose_name=_('Respuesta')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Respuesta de Notificación')
        verbose_name_plural = _('Respuestas de Notificaciones')
        db_table = 'telemetry_telemetry_notification_response'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification.title} - {self.user.username}"


class TelemetryProcessingLog(models.Model):
    """Log de procesamiento de telemetría"""
    
    LOG_TYPES = [
        ('DATA_RECEIVED', 'Datos recibidos'),
        ('DATA_PROCESSED', 'Datos procesados'),
        ('DGA_SENT', 'DGA enviado'),
        ('DGA_RESPONSE', 'Respuesta DGA'),
        ('ERROR', 'Error'),
        ('WARNING', 'Advertencia'),
    ]
    
    catchment_point = models.ForeignKey(
        'catchment.CatchmentPoint',
        on_delete=models.CASCADE,
        related_name='processing_logs',
        verbose_name=_('Punto de captación')
    )
    
    log_type = models.CharField(
        max_length=20,
        choices=LOG_TYPES,
        verbose_name=_('Tipo de log')
    )
    
    message = models.TextField(
        verbose_name=_('Mensaje')
    )
    
    details = models.JSONField(
        default=dict,
        verbose_name=_('Detalles'),
        help_text=_('Detalles adicionales del log')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Log de Procesamiento')
        verbose_name_plural = _('Logs de Procesamiento')
        db_table = 'telemetry_telemetry_processing_log'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.catchment_point.name} - {self.get_log_type_display()} - {self.created_at}"





# ============================================================================
# NUEVOS MODELOS PARA SISTEMA MEJORADO DE ALMACENAMIENTO
# ============================================================================

class RawTelemetryData(models.Model):
    """Datos brutos de telemetría - almacenamiento sin procesar"""
    
    # Punto de captación
    catchment_point = models.ForeignKey(
        'catchment.CatchmentPoint',
        on_delete=models.CASCADE,
        related_name='raw_telemetry_data',
        verbose_name=_('Punto de captación')
    )
    
    # Timestamps
    measurement_time = models.DateTimeField(
        verbose_name=_('Fecha/hora medición')
    )
    
    logger_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Fecha/hora logger')
    )
    
    # Datos brutos - almacenamiento flexible
    raw_data = models.JSONField(
        verbose_name=_('Datos brutos'),
        help_text=_('Datos brutos recibidos del dispositivo')
    )
    
    # Estado de procesamiento
    is_processed = models.BooleanField(
        default=False,
        verbose_name=_('Procesado')
    )
    
    processing_status = models.CharField(
        max_length=20,
        default='PENDING',
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
        verbose_name = _('Dato Bruto de Telemetría')
        verbose_name_plural = _('Datos Brutos de Telemetría')
        db_table = 'telemetry_raw_telemetry_data'
        indexes = [
            models.Index(fields=['catchment_point', 'measurement_time']),
            models.Index(fields=['measurement_time']),
            models.Index(fields=['is_processed']),
            models.Index(fields=['processing_status']),
        ]
        ordering = ['-measurement_time']
    
    def __str__(self):
        return f"{self.catchment_point.name} - {self.measurement_time}"


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
        return self.name


class ProcessingConstant(models.Model):
    """Constantes de procesamiento con fechas de vigencia"""
    
    CONSTANT_TYPES = [
        ('CALIBRATION', 'Calibración'),
        ('CONVERSION', 'Conversión'),
        ('THRESHOLD', 'Umbral'),
        ('OFFSET', 'Desplazamiento'),
        ('MULTIPLIER', 'Multiplicador'),
        ('CUSTOM', 'Personalizado'),
    ]
    
    name = models.CharField(
        max_length=100,
        verbose_name=_('Nombre de la constante')
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_('Descripción')
    )
    
    constant_type = models.CharField(
        max_length=20,
        choices=CONSTANT_TYPES,
        verbose_name=_('Tipo de constante')
    )
    
    # Valor de la constante
    value = models.DecimalField(
        max_digits=15,
        decimal_places=6,
        verbose_name=_('Valor')
    )
    
    # Fechas de vigencia
    start_date = models.DateTimeField(
        verbose_name=_('Fecha de inicio'),
        help_text=_('Fecha desde cuando es válida esta constante')
    )
    
    end_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Fecha de fin'),
        help_text=_('Fecha hasta cuando es válida (vacío = sin límite)')
    )
    
    # Configuración específica
    config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración'),
        help_text=_('Configuración específica de la constante')
    )
    
    # Puntos de captación a los que aplica
    catchment_points = models.ManyToManyField(
        'catchment.CatchmentPoint',
        blank=True,
        related_name='processing_constants',
        verbose_name=_('Puntos de captación')
    )
    
    # Variables a las que aplica
    variables = models.ManyToManyField(
        'variables.Variable',
        blank=True,
        related_name='processing_constants',
        verbose_name=_('Variables')
    )
    
    # Estado
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Activa')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Constante de Procesamiento')
        verbose_name_plural = _('Constantes de Procesamiento')
        db_table = 'telemetry_processing_constant'
        indexes = [
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['constant_type']),
            models.Index(fields=['is_active']),
        ]
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.name} ({self.constant_type})"
    
    def is_valid_for_date(self, date):
        """Verificar si la constante es válida para una fecha específica"""
        if not self.is_active:
            return False
        
        if date < self.start_date:
            return False
        
        if self.end_date and date > self.end_date:
            return False
        
        return True
    
    def is_currently_active(self):
        """Verificar si la constante está actualmente activa"""
        from django.utils import timezone
        now = timezone.now()
        return self.is_valid_for_date(now)


class ProcessedTelemetryData(models.Model):
    """Datos de telemetría procesados según esquemas"""
    
    # Punto de captación
    catchment_point = models.ForeignKey(
        'catchment.CatchmentPoint',
        on_delete=models.CASCADE,
        related_name='processed_telemetry_data',
        verbose_name=_('Punto de captación')
    )
    
    # Esquema aplicado
    response_schema = models.ForeignKey(
        ResponseSchema,
        on_delete=models.CASCADE,
        related_name='processed_data',
        verbose_name=_('Esquema de respuesta')
    )
    
    # Datos brutos originales
    raw_data = models.ForeignKey(
        RawTelemetryData,
        on_delete=models.CASCADE,
        related_name='processed_instances',
        verbose_name=_('Datos brutos originales')
    )
    
    # Timestamps
    measurement_time = models.DateTimeField(
        verbose_name=_('Fecha/hora medición')
    )
    
    # Datos procesados según esquema
    processed_data = models.JSONField(
        verbose_name=_('Datos procesados'),
        help_text=_('Datos procesados según el esquema de respuesta')
    )
    
    # Constantes aplicadas
    applied_constants = models.JSONField(
        default=list,
        verbose_name=_('Constantes aplicadas'),
        help_text=_('Lista de constantes aplicadas en el procesamiento')
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
        verbose_name = _('Dato Procesado de Telemetría')
        verbose_name_plural = _('Datos Procesados de Telemetría')
        db_table = 'telemetry_processed_telemetry_data'
        indexes = [
            models.Index(fields=['catchment_point', 'measurement_time']),
            models.Index(fields=['response_schema', 'measurement_time']),
            models.Index(fields=['measurement_time']),
            models.Index(fields=['processing_status']),
        ]
        ordering = ['-measurement_time']
        unique_together = ['catchment_point', 'response_schema', 'measurement_time']
    
    def __str__(self):
        return f"{self.catchment_point.name} - {self.response_schema.name} - {self.measurement_time}" 