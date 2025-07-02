"""
Modelo de Datos de Telemetría
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


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