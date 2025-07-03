"""Variables App Config"""
from django.apps import AppConfig


class VariablesAppConfig(AppConfig):
    """AppConfig para la app de variables"""
    name = 'api.apps.variables'
    verbose_name = 'Variables'

    def ready(self):
        import api.apps.variables.signals 