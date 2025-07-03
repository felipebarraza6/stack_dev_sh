"""
Configuración de la app de Telemetría
"""
from django.apps import AppConfig


class TelemetryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.apps.telemetry'
    verbose_name = 'Telemetría'
    
    def ready(self):
        """Importar señales cuando la app esté lista"""
        try:
            import api.apps.telemetry.signals
        except ImportError:
            pass 