"""
Modelo de Configuración MQTT
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from ..providers.provider import Provider


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