"""
Signals para la app de catchment
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CatchmentPoint, Project


@receiver(post_save, sender=CatchmentPoint)
def setup_catchment_point(sender, instance, created, **kwargs):
    """Configurar punto de captación"""
    if created:
        # Lógica para configurar punto de captación
        pass


@receiver(post_save, sender=Project)
def setup_project(sender, instance, created, **kwargs):
    """Configurar proyecto"""
    if created:
        # Lógica para configurar proyecto
        pass 