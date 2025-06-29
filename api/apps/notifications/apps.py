from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.apps.notifications'
    verbose_name = 'Notificaciones'

    def ready(self):
        """Importar signals cuando la aplicación esté lista"""
        import api.apps.notifications.signals 