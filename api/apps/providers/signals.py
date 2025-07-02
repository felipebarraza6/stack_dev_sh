"""
Signals para la app de proveedores
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Provider, DeviceToken


@receiver(post_save, sender=Provider)
def update_provider_status(sender, instance, created, **kwargs):
    """Actualizar estado del proveedor"""
    if created:
        # Lógica para inicializar proveedor
        pass


@receiver(post_save, sender=DeviceToken)
def cache_device_token(sender, instance, created, **kwargs):
    """Cachear token de dispositivo"""
    if created and instance.is_active:
        # Lógica para cachear token
        pass 