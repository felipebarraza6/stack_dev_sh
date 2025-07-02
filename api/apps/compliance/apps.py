"""
Configuración de la app de Cumplimiento
"""
from django.apps import AppConfig


class ComplianceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.apps.compliance'
    verbose_name = 'Cumplimiento'
    
    def ready(self):
        """Importar señales cuando la app esté lista"""
        try:
            import api.apps.compliance.signals
        except ImportError:
            pass 