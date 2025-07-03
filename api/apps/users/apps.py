"""Users App Config"""
from django.apps import AppConfig


class UsersAppConfig(AppConfig):
    """AppConfig para la app de usuarios"""
    name = 'api.apps.users'
    verbose_name = 'Usuarios'

    def ready(self):
        import api.apps.users.signals 