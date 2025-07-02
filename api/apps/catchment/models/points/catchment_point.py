"""
Modelo de Punto de Captación
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class CatchmentPoint(models.Model):
    """Punto de captación para telemetría"""
    
    POINT_TYPES = [
        ('WELL', 'Pozo'),
        ('RIVER', 'Río'),
        ('LAKE', 'Lago'),
        ('RESERVOIR', 'Embalse'),
        ('SPRING', 'Manantial'),
        ('DRAIN', 'Drenaje'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Activo'),
        ('INACTIVE', 'Inactivo'),
        ('MAINTENANCE', 'En mantenimiento'),
        ('ERROR', 'Con error'),
        ('OFFLINE', 'Desconectado'),
    ]
    
    name = models.CharField(
        max_length=200,
        verbose_name=_('Nombre')
    )
    
    code = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Código')
    )
    
    point_type = models.CharField(
        max_length=20,
        choices=POINT_TYPES,
        default='WELL',
        verbose_name=_('Tipo de punto')
    )
    
    # Propietario
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_catchment_points',
        verbose_name=_('Propietario')
    )
    
    # Ubicación
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        null=True,
        blank=True,
        verbose_name=_('Latitud')
    )
    
    longitude = models.DecimalField(
        max_digits=11,
        decimal_places=8,
        null=True,
        blank=True,
        verbose_name=_('Longitud')
    )
    
    altitude = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Altitud (m)')
    )
    
    # Configuración de telemetría
    device_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('ID del dispositivo'),
        help_text=_('Identificador único del dispositivo de telemetría')
    )
    
    provider = models.CharField(
        max_length=50,
        verbose_name=_('Proveedor'),
        help_text=_('Proveedor de datos (Twin, Nettra, Novus, etc.)')
    )
    
    # Configuración
    config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración'),
        help_text=_('Configuración específica del punto de captación')
    )
    
    # Estado
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE',
        verbose_name=_('Estado')
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Activo')
    )
    
    # Frecuencia de muestreo
    sampling_frequency = models.IntegerField(
        default=60,
        verbose_name=_('Frecuencia de muestreo (minutos)')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Punto de Captación')
        verbose_name_plural = _('Puntos de Captación')
        db_table = 'catchment_catchment_point'
        indexes = [
            models.Index(fields=['device_id']),
            models.Index(fields=['provider']),
            models.Index(fields=['status']),
            models.Index(fields=['owner']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    @property
    def location_display(self):
        """Mostrar ubicación en formato legible"""
        if self.latitude and self.longitude:
            return f"{self.latitude}, {self.longitude}"
        return "Sin ubicación" 