"""
Modelos de Cumplimiento para Telemetría
Sistema enfocado en cumplimiento de normativas para datos de telemetría
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class ComplianceSource(models.Model):
    """Fuente de cumplimiento (DGA, SMA, etc.)"""
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Nombre de la fuente')
    )
    
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_('Código de la fuente')
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_('Descripción')
    )
    
    # Configuración de la fuente
    config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración'),
        help_text=_('Configuración específica de la fuente de cumplimiento')
    )
    
    # Variables que maneja esta fuente
    supported_variables = models.JSONField(
        default=list,
        verbose_name=_('Variables soportadas'),
        help_text=_('Lista de variables que maneja esta fuente')
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
        verbose_name = _('Fuente de Cumplimiento')
        verbose_name_plural = _('Fuentes de Cumplimiento')
        db_table = 'compliance_compliance_source'
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class ComplianceConfig(models.Model):
    """Configuración de cumplimiento para un punto de captación"""
    
    catchment_point = models.ForeignKey(
        'catchment.CatchmentPoint',
        on_delete=models.CASCADE,
        related_name='compliance_configs',
        verbose_name=_('Punto de captación')
    )
    
    compliance_source = models.ForeignKey(
        ComplianceSource,
        on_delete=models.CASCADE,
        related_name='configs',
        verbose_name=_('Fuente de cumplimiento')
    )
    
    # Configuración específica
    config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración específica'),
        help_text=_('Configuración específica para este punto y fuente')
    )
    
    # Estado
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Activo')
    )
    
    # Fechas de cumplimiento
    start_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Fecha de inicio')
    )
    
    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Fecha de fin')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Configuración de Cumplimiento')
        verbose_name_plural = _('Configuraciones de Cumplimiento')
        db_table = 'compliance_compliance_config'
        unique_together = ['catchment_point', 'compliance_source']
    
    def __str__(self):
        return f"{self.catchment_point.name} - {self.compliance_source.name}"


class ComplianceData(models.Model):
    """Datos de cumplimiento enviados"""
    
    compliance_config = models.ForeignKey(
        ComplianceConfig,
        on_delete=models.CASCADE,
        related_name='data_sent',
        verbose_name=_('Configuración de cumplimiento')
    )
    
    # Datos enviados
    data = models.JSONField(
        verbose_name=_('Datos enviados'),
        help_text=_('Datos enviados a la fuente de cumplimiento')
    )
    
    # Estado del envío
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pendiente'),
            ('SENT', 'Enviado'),
            ('CONFIRMED', 'Confirmado'),
            ('REJECTED', 'Rechazado'),
            ('ERROR', 'Error'),
        ],
        default='PENDING',
        verbose_name=_('Estado')
    )
    
    # Respuesta de la fuente
    response = models.JSONField(
        default=dict,
        verbose_name=_('Respuesta'),
        help_text=_('Respuesta de la fuente de cumplimiento')
    )
    
    # Metadata
    sent_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Confirmado el')
    )
    
    class Meta:
        verbose_name = _('Dato de Cumplimiento')
        verbose_name_plural = _('Datos de Cumplimiento')
        db_table = 'compliance_compliance_data'
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.compliance_config} - {self.sent_at}"


class ComplianceLog(models.Model):
    """Log de actividades de cumplimiento"""
    
    compliance_config = models.ForeignKey(
        ComplianceConfig,
        on_delete=models.CASCADE,
        related_name='logs',
        verbose_name=_('Configuración de cumplimiento')
    )
    
    # Tipo de actividad
    activity_type = models.CharField(
        max_length=20,
        choices=[
            ('CONFIGURED', 'Configurado'),
            ('DATA_SENT', 'Datos enviados'),
            ('DATA_RECEIVED', 'Datos recibidos'),
            ('ERROR', 'Error'),
            ('NOTIFICATION', 'Notificación'),
        ],
        verbose_name=_('Tipo de actividad')
    )
    
    # Detalles de la actividad
    details = models.JSONField(
        default=dict,
        verbose_name=_('Detalles'),
        help_text=_('Detalles de la actividad')
    )
    
    # Estado
    status = models.CharField(
        max_length=20,
        choices=[
            ('SUCCESS', 'Exitoso'),
            ('WARNING', 'Advertencia'),
            ('ERROR', 'Error'),
        ],
        verbose_name=_('Estado')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Log de Cumplimiento')
        verbose_name_plural = _('Logs de Cumplimiento')
        db_table = 'compliance_compliance_log'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.compliance_config} - {self.activity_type} - {self.created_at}" 