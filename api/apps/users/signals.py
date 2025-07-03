"""
Signals para la app de usuarios
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from api.apps.users.models.users.user import User
# from api.apps.users.models.users.user_profile import UserProfile  # No existe este modelo


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crear perfil de usuario automáticamente"""
    if created:
        # UserProfile.objects.create(user=instance)  # Comentado porque no existe el modelo
        pass


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Guardar perfil de usuario"""
    # if hasattr(instance, 'profile'):  # Comentado porque no existe el modelo
    #     instance.profile.save()
    pass 