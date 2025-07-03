"""
Signals para la app de variables
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from api.apps.variables.models.variables.variable import Variable
from api.apps.variables.models.alerts.alert import VariableAlert


@receiver(post_save, sender=Variable)
def update_variable_cache(sender, instance, created, **kwargs):
    """Actualizar caché de variables"""
    if created:
        # Lógica para actualizar caché
        pass


@receiver(post_save, sender=VariableAlert)
def setup_alert_monitoring(sender, instance, created, **kwargs):
    """Configurar monitoreo de alertas"""
    if created and instance.is_active:
        # Lógica para configurar monitoreo
        pass 