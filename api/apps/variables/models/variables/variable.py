"""
Modelo de Variable Individual
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Variable(models.Model):
    """Variable individual con configuración avanzada"""
    
    VARIABLE_TYPES = [
        ('NIVEL', 'Nivel'),
        ('CAUDAL', 'Caudal'),
        ('CAUDAL_PROMEDIO', 'Caudal Promedio'),
        ('TOTALIZADO', 'Totalizado'),
        ('TEMPERATURA', 'Temperatura'),
        ('PRESION', 'Presión'),
        ('PH', 'pH'),
        ('CONDUCTIVIDAD', 'Conductividad'),
        ('TURBIDEZ', 'Turbidez'),
        ('CUSTOM', 'Personalizado'),
    ]
    
    UNIT_TYPES = [
        ('METERS', 'Metros'),
        ('LITERS_PER_SECOND', 'L/s'),
        ('CUBIC_METERS', 'm³'),
        ('CUBIC_METERS_PER_HOUR', 'm³/h'),
        ('CELSIUS', '°C'),
        ('BAR', 'Bar'),
        ('PH_UNITS', 'pH'),
        ('MICROSIEMENS', 'μS/cm'),
        ('NTU', 'NTU'),
        ('CUSTOM', 'Personalizado'),
    ]
    
    name = models.CharField(
        max_length=100,
        verbose_name=_('Nombre de la variable')
    )
    
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Código de la variable')
    )
    
    variable_type = models.CharField(
        max_length=20,
        choices=VARIABLE_TYPES,
        verbose_name=_('Tipo de variable')
    )
    
    unit = models.CharField(
        max_length=20,
        choices=UNIT_TYPES,
        verbose_name=_('Unidad de medida')
    )
    
    custom_unit = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('Unidad personalizada')
    )
    
    # Configuración de procesamiento
    processing_config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración de procesamiento'),
        help_text=_('Configuración específica de procesamiento para esta variable')
    )
    
    # Límites y rangos
    min_value = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name=_('Valor mínimo')
    )
    
    max_value = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name=_('Valor máximo')
    )
    
    # Configuración de alertas
    alert_config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración de alertas'),
        help_text=_('Configuración de alertas para esta variable')
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
        verbose_name = _('Variable')
        verbose_name_plural = _('Variables')
        db_table = 'variables_variable'
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_unit_display(self):
        """Obtener la unidad de medida para mostrar"""
        if self.unit == 'CUSTOM' and self.custom_unit:
            return self.custom_unit
        return self.get_unit_display() 