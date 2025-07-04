# Funcionamiento de Modelos y Tareas del Sistema

## 📊 Arquitectura de Modelos

### 🏗️ Modelos Base (Herencia)

El sistema utiliza una arquitectura de herencia de modelos para mantener consistencia y reutilizar funcionalidades comunes:

#### 1. BaseModel (Core)

```python
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']
```

**Funcionalidades heredadas:**

- **Auditoría automática**: `created_at`, `updated_at`
- **Estado activo**: `is_active`
- **Ordenamiento**: Por fecha de creación descendente
- **Métodos útiles**: `is_recent`, `age_days`

#### 2. TimestampedModel (Core)

```python
class TimestampedModel(BaseModel):
    timestamp = models.DateTimeField()
    device_timestamp = models.DateTimeField(null=True)
```

**Campos adicionales:**

- **timestamp**: Timestamp del sistema
- **device_timestamp**: Timestamp del dispositivo
- **Método**: `time_difference()` - diferencia entre timestamps

#### 3. SoftDeleteModel (Core)

```python
class SoftDeleteModel(BaseModel):
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey('users.User', null=True)
```

**Funcionalidades:**

- **Soft delete**: Marcar como eliminado sin borrar
- **Métodos**: `soft_delete()`, `restore()`, `hard_delete()`

### 🔗 Relaciones entre Aplicaciones

#### Diagrama de Relaciones Principales

```
CatchmentPoint (catchment)
├── TelemetryData (telemetry) - OneToMany
├── ComplianceConfig (compliance) - OneToMany
├── VariableDataPoint (variables) - OneToMany
├── Provider (providers) - ManyToMany
└── ProcessingConfig (catchment) - OneToOne

Variable (variables)
├── VariableDataPoint (variables) - OneToMany
├── ProcessingConstant (telemetry) - ManyToMany
└── VariableSchema (variables) - ManyToMany

ComplianceSource (compliance)
└── ComplianceConfig (compliance) - OneToMany

ResponseSchema (telemetry)
└── ProcessedTelemetryData (telemetry) - OneToMany
```

#### Relaciones Detalladas

##### 1. CatchmentPoint (Punto de Captación)

**Ubicación**: `api/apps/catchment/models/points/catchment_point.py`

**Relaciones principales:**

- **TelemetryData**: Un punto puede tener múltiples datos de telemetría
- **ComplianceConfig**: Un punto puede tener múltiples configuraciones de cumplimiento
- **VariableDataPoint**: Un punto puede tener múltiples puntos de datos de variables
- **Provider**: Un punto puede estar conectado a múltiples proveedores
- **ProcessingConfig**: Un punto tiene una configuración de procesamiento

##### 2. TelemetryData (Datos de Telemetría)

**Ubicación**: `api/apps/telemetry/models/models.py`

**Campos principales:**

```python
class TelemetryData(models.Model):
    catchment_point = models.ForeignKey('catchment.CatchmentPoint')
    measurement_time = models.DateTimeField()
    flow = models.DecimalField()  # Caudal (l/s)
    total = models.DecimalField()  # Total (m³)
    level = models.DecimalField()  # Nivel (m)
    water_table = models.DecimalField()  # Nivel freático (m)
    send_dga = models.BooleanField()  # Estado envío DGA
```

**Relaciones:**

- **CatchmentPoint**: Cada dato pertenece a un punto de captación
- **RawTelemetryData**: Datos brutos originales
- **ProcessedTelemetryData**: Datos procesados según esquemas

##### 3. Variable (Variables del Sistema)

**Ubicación**: `api/apps/variables/models/variables/variable.py`

**Tipos de variables:**

- NIVEL, CAUDAL, CAUDAL_PROMEDIO, TOTALIZADO
- TEMPERATURA, PRESION, PH, CONDUCTIVIDAD, TURBIDEZ
- CUSTOM (personalizado)

**Configuración:**

- **Unidades**: Metros, L/s, m³, °C, Bar, pH, etc.
- **Límites**: min_value, max_value
- **Alertas**: alert_config (JSON)
- **Procesamiento**: processing_config (JSON)

##### 4. ComplianceConfig (Configuración de Cumplimiento)

**Ubicación**: `api/apps/compliance/models/configs/compliance_config.py`

**Hereda de**: BaseModel

**Relaciones:**

- **CatchmentPoint**: Punto de captación asociado
- **ComplianceSource**: Fuente de cumplimiento (DGA, etc.)
- **ComplianceData**: Datos enviados a cumplimiento

## ⏰ Sistema de Tareas (Celery)

### 🏗️ Arquitectura de Tareas

El sistema utiliza Celery para procesamiento asíncrono con configuración modular por entornos:

#### Estructura de Archivos

```
api/tasks/
├── __init__.py              # Exporta todas las tareas
├── telemetry.py             # Tareas de telemetría
├── compliance.py            # Tareas de cumplimiento
├── notifications.py         # Tareas de notificaciones
└── config/
    ├── base.py              # Configuración común
    ├── development.py       # Configuración desarrollo
    └── production.py        # Configuración producción
```

### 📅 Configuración de Tareas Programadas

#### Configuración Base (`config/base.py`)

```python
CELERY_BEAT_SCHEDULE = {
    # Telemetría
    'sync-telemetry-sources': {
        'task': 'api.tasks.telemetry.sync_telemetry_sources',
        'schedule': crontab(minute='*/5'),  # Cada 5 minutos
    },
    'health-check': {
        'task': 'api.tasks.telemetry.health_check',
        'schedule': crontab(minute='*/10'),  # Cada 10 minutos
    },
    'cleanup-old-data': {
        'task': 'api.tasks.telemetry.cleanup_old_data',
        'schedule': crontab(hour=2, minute=0),  # Diario a las 2:00 AM
    },

    # Cumplimiento
    'daily-compliance-report': {
        'task': 'api.tasks.compliance.daily_compliance_report',
        'schedule': crontab(hour=7, minute=0),  # Diario a las 7:00 AM
    },
    'sync-compliance-sources': {
        'task': 'api.tasks.compliance.sync_compliance_sources',
        'schedule': crontab(hour='*/2'),  # Cada 2 horas
    },

    # Notificaciones
    'send-daily-summary': {
        'task': 'api.tasks.notifications.send_daily_summary',
        'schedule': crontab(hour=8, minute=0),  # Diario a las 8:00 AM
    },
}
```

#### Diferencias por Entorno

| Tarea                   | Desarrollo | Producción |
| ----------------------- | ---------- | ---------- |
| Sync Telemetría         | 15 min     | 2 min      |
| Health Check            | 30 min     | 5 min      |
| Validación Telemetría   | 45 min     | 10 min     |
| Sync Cumplimiento       | 4 horas    | 1 hora     |
| Validación Cumplimiento | 1 hora     | 15 min     |

### 🔧 Tareas Principales

#### 1. Tareas de Telemetría (`telemetry.py`)

##### `process_telemetry_data`

```python
@shared_task(bind=True, max_retries=3)
def process_telemetry_data(self, catchment_point_id, data_source='mqtt'):
    """Procesa datos de telemetría para un punto de captación"""
    catchment_point = CatchmentPoint.objects.get(id=catchment_point_id)
    processor = TelemetryProcessor(catchment_point)
    result = processor.process_data(data_source)
    return result
```

**Funcionalidad:**

- Procesa datos de telemetría para un punto específico
- Utiliza el procesador configurado para el punto
- Registra métricas de procesamiento
- Maneja reintentos automáticos

##### `health_check`

```python
@shared_task
def health_check():
    """Verificación de salud del sistema de telemetría"""
    metrics = TelemetryMetrics()
    health_status = metrics.check_system_health()
    return health_status
```

**Funcionalidad:**

- Verifica el estado general del sistema
- Monitorea conectividad con dispositivos
- Valida integridad de datos
- Genera alertas si es necesario

##### `cleanup_old_data`

```python
@shared_task
def cleanup_old_data():
    """Limpia datos antiguos del sistema de telemetría"""
    cutoff_date = timezone.now() - timedelta(days=30)
    # Limpiar datos antiguos
```

**Funcionalidad:**

- Elimina datos de telemetría antiguos (>30 días)
- Limpia logs de procesamiento
- Optimiza rendimiento de base de datos

#### 2. Tareas de Cumplimiento (`compliance.py`)

##### `send_compliance_data`

```python
@shared_task(bind=True, max_retries=3)
def send_compliance_data(self, compliance_config_id):
    """Envía datos de cumplimiento a la fuente correspondiente"""
    compliance_config = ComplianceConfig.objects.get(id=compliance_config_id)
    catchment_point = compliance_config.catchment_point
    processor = TelemetryProcessor(catchment_point)

    # Preparar datos según esquema requerido
    source = compliance_config.compliance_source
    data = processor.prepare_compliance_data(source.required_schema)

    # Enviar datos
    response = processor.send_to_compliance_source(source, data)

    # Registrar envío
    ComplianceData.objects.create(
        compliance_config=compliance_config,
        data=data,
        status='SENT',
        response=response
    )
```

**Funcionalidad:**

- Envía datos de cumplimiento a fuentes externas (DGA, etc.)
- Prepara datos según esquemas requeridos
- Registra envíos y respuestas
- Maneja reintentos automáticos

##### `daily_compliance_report`

```python
@shared_task
def daily_compliance_report():
    """Genera reporte diario de cumplimiento"""
    configs = ComplianceConfig.objects.filter(is_active=True)
    for config in configs:
        generate_compliance_report.delay(config.id, date.today())
```

**Funcionalidad:**

- Genera reportes diarios de cumplimiento
- Procesa todas las configuraciones activas
- Envía reportes a fuentes correspondientes

#### 3. Tareas de Notificaciones (`notifications.py`)

##### `notify_compliance_users`

```python
@shared_task
def notify_compliance_users(compliance_config_id, notification_type, details):
    """Notifica a usuarios sobre eventos de cumplimiento"""
    compliance_config = ComplianceConfig.objects.get(id=compliance_config_id)
    notifications = CatchmentPointNotification.objects.filter(
        catchment_point=compliance_config.catchment_point,
        is_active=True
    )

    for notification in notifications:
        if notification_type in notification.notification_types:
            for channel in notification.channels:
                if channel == 'EMAIL':
                    send_email_notification.delay(notification.user.id, notification_type, details)
                elif channel == 'SMS':
                    send_sms_notification.delay(notification.user.id, notification_type, details)
```

**Funcionalidad:**

- Notifica a usuarios sobre eventos de cumplimiento
- Soporta múltiples canales (email, SMS)
- Filtra por tipos de notificación
- Envía notificaciones personalizadas

### ⚙️ Configuración de Celery

#### Configuración Base (`config/celery.py`)

```python
app = Celery('stack_vps')

app.conf.update(
    broker_url=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    result_backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),

    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Santiago',
    enable_utc=True,

    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,

    task_acks_late=True,
    task_reject_on_worker_lost=True,
)
```

#### Rutas de Tareas

```python
app.conf.task_routes = {
    'tasks.telemetry.*': {'queue': 'telemetry'},
    'tasks.compliance.*': {'queue': 'compliance'},
    'tasks.notifications.*': {'queue': 'notifications'},
    'tasks.reports.*': {'queue': 'reports'},
}
```

### 📊 Monitoreo y Métricas

#### Logging de Tareas

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

#### Métricas de Rendimiento

- **Tiempo de ejecución**: Soft limit 5 min, hard limit 10 min
- **Reintentos**: Máximo 3 reintentos con backoff exponencial
- **Concurrencia**: 8 workers en producción con autoscaling
- **Colas**: Separación por tipo de tarea para mejor control

### 🔄 Flujo de Datos Completo

#### 1. Recepción de Datos

```
Dispositivo → MQTT → RawTelemetryData → Tarea process_telemetry_data
```

#### 2. Procesamiento

```
RawTelemetryData → TelemetryProcessor → TelemetryData + ProcessedTelemetryData
```

#### 3. Cumplimiento

```
TelemetryData → ComplianceProcessor → ComplianceData → Tarea send_compliance_data
```

#### 4. Notificaciones

```
Eventos → Tarea notify_compliance_users → Email/SMS → Usuarios
```

### 📋 Planificación y Consideraciones

#### Para Desarrollo

- **Frecuencias reducidas**: Menos carga en desarrollo
- **Límites de tiempo extendidos**: Más tiempo para debugging
- **Logging detallado**: Para facilitar troubleshooting
- **Rate limits deshabilitados**: Para testing

#### Para Producción

- **Frecuencias aumentadas**: Respuesta rápida del sistema
- **Límites de tiempo estrictos**: Control de recursos
- **Logging optimizado**: Para rendimiento
- **Autoscaling**: Adaptación automática a carga

#### Consideraciones de Escalabilidad

- **Separación de colas**: Por tipo de tarea
- **Workers especializados**: Por dominio
- **Monitoreo continuo**: Métricas de rendimiento
- **Backup de datos**: Antes de limpieza automática

### 🚀 Beneficios del Sistema

1. **Modularidad**: Tareas organizadas por dominio
2. **Escalabilidad**: Configuración por entorno
3. **Confiabilidad**: Reintentos automáticos
4. **Monitoreo**: Logging y métricas detalladas
5. **Flexibilidad**: Configuración dinámica
6. **Mantenibilidad**: Código organizado y documentado
