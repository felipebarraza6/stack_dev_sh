"""Catchment App Config"""
from django.apps import AppConfig


class CatchmentAppConfig(AppConfig):
    """AppConfig para la app de catchment"""
    name = 'api.apps.catchment'
    verbose_name = 'Puntos de Captación'

    def ready(self):
        import api.apps.catchment.signals 