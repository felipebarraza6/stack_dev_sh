"""
Tareas de Celery organizadas por módulos
Sistema modular de procesamiento asíncrono
"""

# Importar tareas de telemetría
from .telemetry import (
    process_telemetry_data,
    health_check,
    cleanup_old_data,
)

# Importar tareas de cumplimiento
from .compliance import (
    send_compliance_data,
    daily_compliance_report,
    generate_compliance_report,
    sync_compliance_sources,
    sync_with_source,
)

# Importar tareas de notificaciones
from .notifications import (
    notify_compliance_users,
    send_email_notification,
    send_sms_notification,
)

# Exportar todas las tareas
__all__ = [
    # Telemetría
    'process_telemetry_data',
    'health_check',
    'cleanup_old_data',
    
    # Cumplimiento
    'send_compliance_data',
    'daily_compliance_report',
    'generate_compliance_report',
    'sync_compliance_sources',
    'sync_with_source',
    
    # Notificaciones
    'notify_compliance_users',
    'send_email_notification',
    'send_sms_notification',
] 