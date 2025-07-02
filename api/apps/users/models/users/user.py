"""
Modelos de Usuarios para Telemetría
Sistema simplificado de gestión de usuarios enfocado en telemetría
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Usuario del sistema con campos básicos para telemetría"""
    
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _('El usuario ya existe.')
        }
    )
    
    # Campos básicos para telemetría
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name=_('Teléfono')
    )
    
    company = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_('Empresa')
    )
    
    # Configuración de notificaciones
    email_notifications = models.BooleanField(
        default=True,
        verbose_name=_('Notificaciones por email')
    )
    
    sms_notifications = models.BooleanField(
        default=False,
        verbose_name=_('Notificaciones por SMS')
    )
    
    # Configuración
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        db_table = 'users_user'
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        return self.first_name or self.email 