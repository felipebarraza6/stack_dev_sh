# Sistema Modular de Tareas de Celery

## Estructura de Tareas Organizadas

El sistema de tareas de Celery ahora está organizado de manera modular para facilitar el mantenimiento y escalabilidad.

### Estructura de Archivos

```
api/tasks/
├── __init__.py              # Exporta todas las tareas organizadas
├── telemetry.py             # Tareas específicas de telemetría
├── compliance.py            # Tareas específicas de cumplimiento
├── notifications.py         # Tareas específicas de notificaciones
└── config/
    ├── __init__.py          # Exporta configuración base
    ├── base.py              # Configuración común para todos los entornos
    ├── development.py       # Configuración específica para desarrollo
    └── production.py        # Configuración específica para producción
```

## Módulos de Tareas

### 1. Tareas de Telemetría (`telemetry.py`)

Tareas relacionadas con el procesamiento de datos de telemetría:

- **`process_telemetry_data`**: Procesa datos de telemetría para un punto de captación
- **`cleanup_old_data`**: Limpia datos antiguos del sistema de telemetría
- **`health_check`**: Verificación de salud del sistema de telemetría
- **`sync_telemetry_sources`**: Sincroniza con fuentes de datos de telemetría
- **`validate_telemetry_data`**: Valida la integridad de los datos de telemetría
- **`generate_telemetry_report`**: Genera reporte de telemetría del día

### 2. Tareas de Cumplimiento (`compliance.py`)

Tareas relacionadas con el cumplimiento regulatorio:

- **`send_compliance_data`**: Envía datos de cumplimiento a la fuente correspondiente
- **`daily_compliance_report`**: Genera reporte diario de cumplimiento
- **`generate_compliance_report`**: Genera reporte específico de cumplimiento
- **`sync_compliance_sources`**: Sincroniza con fuentes de cumplimiento externas
- **`sync_with_source`**: Sincroniza con una fuente específica de cumplimiento
- **`validate_compliance_data`**: Valida la integridad de los datos de cumplimiento
- **`cleanup_compliance_logs`**: Limpia logs antiguos de cumplimiento

### 3. Tareas de Notificaciones (`notifications.py`)

Tareas relacionadas con el envío de notificaciones:

- **`notify_compliance_users`**: Notifica a usuarios sobre eventos de cumplimiento
- **`send_email_notification`**: Envía notificación por email
- **`send_sms_notification`**: Envía notificación por SMS
- **`send_system_alert`**: Envía alertas del sistema a administradores
- **`send_daily_summary`**: Envía resumen diario a usuarios suscritos

## Configuración por Entornos

### Configuración Base (`config/base.py`)

Configuración común para todos los entornos:

- **Frecuencias estándar**: Configuración base de tareas programadas
- **Timezone**: America/Santiago
- **Límites de tiempo**: 5-10 minutos por tarea
- **Reintentos**: Configuración de reintentos automáticos

### Configuración de Desarrollo (`config/development.py`)

Configuración más permisiva para facilitar el desarrollo:

- **Frecuencias reducidas**: Tareas menos frecuentes para desarrollo
- **Límites de tiempo extendidos**: 10-20 minutos por tarea
- **Rate limits deshabilitados**: Para facilitar testing
- **Prefetch reducido**: Mejor control de recursos

### Configuración de Producción (`config/production.py`)

Configuración más estricta y eficiente para producción:

- **Frecuencias aumentadas**: Tareas más frecuentes para producción
- **Límites de tiempo estrictos**: 5-10 minutos por tarea
- **Rate limits habilitados**: Protección contra sobrecarga
- **Concurrencia optimizada**: 8 workers con autoscaling

## Frecuencias de Tareas por Entorno

### Desarrollo

- **Sync Telemetría**: Cada 15 minutos
- **Health Check**: Cada 30 minutos
- **Validación Telemetría**: Cada 45 minutos
- **Sync Cumplimiento**: Cada 4 horas
- **Validación Cumplimiento**: Cada hora

### Producción

- **Sync Telemetría**: Cada 2 minutos
- **Health Check**: Cada 5 minutos
- **Validación Telemetría**: Cada 10 minutos
- **Sync Cumplimiento**: Cada hora
- **Validación Cumplimiento**: Cada 15 minutos

## Uso de Tareas

### Importación de Tareas

```python
# Importar tareas específicas
from api.tasks.telemetry import process_telemetry_data, health_check
from api.tasks.compliance import send_compliance_data
from api.tasks.notifications import send_email_notification

# O importar todas las tareas
from api.tasks import (
    process_telemetry_data,
    send_compliance_data,
    send_email_notification
)
```

### Ejecución de Tareas

```python
# Ejecutar tarea inmediatamente
result = process_telemetry_data.delay(catchment_point_id, 'mqtt')

# Ejecutar tarea programada
from datetime import timedelta
result = process_telemetry_data.apply_async(
    args=[catchment_point_id, 'mqtt'],
    countdown=60  # Ejecutar en 1 minuto
)

# Ejecutar tarea con retry
result = send_compliance_data.apply_async(
    args=[config_id],
    retry=True,
    retry_policy={
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.2,
    }
)
```

## Configuración Automática

### Variables de Entorno

```bash
# Para desarrollo
export DJANGO_SETTINGS_MODULE=api.config.settings.development

# Para producción
export DJANGO_SETTINGS_MODULE=api.config.settings.production
```

### Docker

```yaml
# docker-compose.yml
environment:
  - DJANGO_SETTINGS_MODULE=api.config.settings.development
```

## Monitoreo y Logging

### Logging de Tareas

```python
import logging
logger = logging.getLogger(__name__)

@shared_task
def my_task():
    logger.info("Tarea iniciada")
    try:
        # Procesamiento
        logger.info("Tarea completada exitosamente")
    except Exception as e:
        logger.error(f"Error en tarea: {e}")
        raise
```

### Monitoreo de Tareas

```python
# Verificar estado de tarea
result = process_telemetry_data.delay(point_id)
print(f"Estado: {result.status}")
print(f"Resultado: {result.get()}")

# Monitorear tareas programadas
from celery.task.control import inspect
i = inspect()
scheduled = i.scheduled()
active = i.active()
reserved = i.reserved()
```

## Beneficios de la Estructura Modular

1. **Separación de Responsabilidades**: Cada módulo maneja un dominio específico
2. **Mantenimiento Fácil**: Cambios centralizados en archivos específicos
3. **Escalabilidad**: Fácil agregar nuevas tareas y módulos
4. **Configuración Automática**: Diferentes configuraciones según el entorno
5. **Testing Simplificado**: Tareas organizadas facilitan las pruebas
6. **Monitoreo Mejorado**: Logging y métricas específicas por módulo

## Extensibilidad

Para agregar un nuevo módulo de tareas:

1. Crear archivo `api/tasks/nuevo_modulo.py`
2. Definir tareas con `@shared_task`
3. Actualizar `api/tasks/__init__.py`
4. Agregar configuración en `api/tasks/config/base.py`
5. Personalizar por entorno si es necesario

```python
# api/tasks/nuevo_modulo.py
from celery import shared_task

@shared_task
def nueva_tarea():
    # Implementación
    pass
```

## Consideraciones de Rendimiento

### Desarrollo

- Tareas menos frecuentes para reducir carga
- Límites de tiempo más permisivos
- Logging detallado para debugging

### Producción

- Tareas más frecuentes para respuesta rápida
- Límites de tiempo estrictos
- Logging optimizado para rendimiento
- Autoscaling de workers
