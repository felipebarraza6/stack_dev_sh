"""
Modelo de Token de Dispositivo
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from ..providers.provider import Provider


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
        return f"{self.provider.name} - {self.device_id}" 