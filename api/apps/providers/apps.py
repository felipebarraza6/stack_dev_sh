"""Providers App Config"""
from django.apps import AppConfig


class ProvidersAppConfig(AppConfig):
    """AppConfig para la app de proveedores"""
    name = 'api.apps.providers'
    verbose_name = 'Proveedores'

    def ready(self):
        import api.apps.providers.signals 