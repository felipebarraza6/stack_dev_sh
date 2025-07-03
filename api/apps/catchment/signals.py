"""
Signals para la app de catchment
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from api.apps.catchment.models.points.catchment_point import CatchmentPoint
# from api.apps.catchment.models.projects.project import Project  # Comentado si no existe


@receiver(post_save, sender=CatchmentPoint)
def setup_catchment_point(sender, instance, created, **kwargs):
    """Configurar punto de captación"""
    if created:
        # Lógica para configurar punto de captación
        pass


# @receiver(post_save, sender=Project)  # Comentado porque no existe el modelo
# def setup_project(sender, instance, created, **kwargs):
#     """Configurar proyecto"""
#     if created:
#         # Lógica para configurar proyecto
#         pass 