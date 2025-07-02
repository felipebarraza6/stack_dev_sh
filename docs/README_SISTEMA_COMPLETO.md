# 🚀 Stack VPS - Sistema Completo de Telemetría y Cumplimiento

## 📋 Resumen del Sistema

Stack VPS es un sistema modular y profesional para la gestión de telemetría de puntos de captación, con capacidades avanzadas de cumplimiento regulatorio (DGA, SMA, etc.) y notificaciones inteligentes.

## 🏗️ Arquitectura Modular

### Apps Principales

1. **`core`** - Funcionalidades centrales del sistema
2. **`users`** - Gestión de usuarios y propietarios de puntos de captación
3. **`providers`** - Sistema dinámico de proveedores de datos
4. **`variables`** - Procesamiento inteligente de variables
5. **`catchment`** - Gestión de puntos de captación
6. **`compliance`** - Sistema de cumplimiento regulatorio dinámico
7. **`telemetry`** - Procesamiento de datos de telemetría

## 🎯 Características Principales

### ✅ Sistema de Cumplimiento Dinámico

- **Fuentes múltiples**: DGA, SMA, y futuras fuentes
- **Esquemas configurables**: Cada fuente define su esquema de datos
- **Envío automático**: Datos procesados y enviados automáticamente
- **Reglas de cumplimiento**: Sistema de reglas configurable
- **Logs completos**: Auditoría de todas las actividades

### ✅ Gestión de Usuarios Avanzada

- **Propietarios de puntos**: Usuarios propietarios de puntos de captación
- **Notificaciones por punto**: Lista de usuarios a notificar por cada punto
- **Roles y permisos**: Sistema granular de permisos
- **Múltiples canales**: Email, SMS, Webhook, In-app

### ✅ Sistema Profesional de Tareas

- **Celery**: Reemplaza cron jobs con sistema profesional
- **Colas separadas**: Telemetría, cumplimiento, notificaciones
- **Retry automático**: Reintentos inteligentes en caso de fallo
- **Monitoreo**: Flower para monitoreo de tareas
- **Escalabilidad**: Workers independientes por tipo de tarea

### ✅ Infraestructura Docker

- **Desarrollo local**: `dev.yml` con SQLite
- **Producción**: `production.yml` con PostgreSQL
- **Servicios incluidos**: Redis, MQTT, Nginx, Celery
- **Monitoreo**: Grafana + Prometheus

## 🚀 Inicio Rápido

### Desarrollo Local

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd stack_vps

# 2. Verificar el sistema
python verificar_sistema_completo.py

# 3. Levantar en desarrollo
./run-dev.sh
```

### URLs Disponibles (Desarrollo)

- **API Django**: http://localhost:8000
- **Nginx**: http://localhost:80
- **Flower (Celery)**: http://localhost:5555
- **Redis**: localhost:6379
- **MQTT**: localhost:1883

## 📊 Estructura de Datos

### Sistema de Cumplimiento

```python
# Fuente de cumplimiento (DGA, SMA, etc.)
ComplianceSource:
  - name: "DGA"
  - code: "dga"
  - required_schema: {...}
  - supported_variables: [...]

# Configuración por punto de captación
ComplianceConfig:
  - catchment_point: FK
  - compliance_source: FK
  - config: JSON
  - start_date/end_date: Date

# Datos enviados
ComplianceData:
  - compliance_config: FK
  - data: JSON
  - status: PENDING/SENT/CONFIRMED/REJECTED/ERROR
  - response: JSON
```

### Gestión de Usuarios

```python
# Propietario de punto de captación
CatchmentPointOwner:
  - user: FK
  - catchment_point: FK
  - ownership_type: PRIMARY/SECONDARY/ADMINISTRATOR
  - permissions: JSON

# Notificaciones por punto
CatchmentPointNotification:
  - catchment_point: FK
  - user: FK
  - notification_types: JSON
  - channels: JSON
```

## 🔧 Configuración

### Variables de Entorno

```bash
# Base de datos
DATABASE_URL=sqlite:///db.sqlite3  # Desarrollo
DATABASE_URL=postgresql://...       # Producción

# Redis
REDIS_URL=redis://localhost:6379/0

# MQTT
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_USERNAME=
MQTT_PASSWORD=

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
```

### Configuración de Celery

```python
# Tareas programadas
beat_schedule = {
    'daily-compliance-report': {
        'task': 'tasks.telemetry.daily_compliance_report',
        'schedule': 86400.0,  # 24 horas
    },
    'health-check': {
        'task': 'tasks.telemetry.health_check',
        'schedule': 3600.0,   # 1 hora
    },
    'sync-compliance-sources': {
        'task': 'tasks.telemetry.sync_compliance_sources',
        'schedule': 21600.0,  # 6 horas
    },
}
```

## 📈 Monitoreo y Métricas

### Health Checks

- Verificación automática de servicios
- Métricas de rendimiento
- Alertas de estado

### Logs Estructurados

- Logs de cumplimiento
- Logs de telemetría
- Logs de notificaciones

### Métricas Prometheus

- Métricas de procesamiento
- Métricas de envío de datos
- Métricas de errores

## 🔄 Migración desde Sistema Anterior

### Plan de Migración Gradual

1. **Fase 1**: Instalación de apps modulares
2. **Fase 2**: Migración de datos existentes
3. **Fase 3**: Configuración de cumplimiento dinámico
4. **Fase 4**: Activación de Celery
5. **Fase 5**: Desactivación de cron jobs

### Scripts de Migración

```bash
# Verificar sistema
python verificar_sistema_completo.py

# Migrar datos
python migrate_to_modular_system.py

# Verificar migración
python verificar_sistema.py
```

## 🛠️ Comandos Útiles

### Desarrollo

```bash
# Ver logs en tiempo real
docker-compose -f dev.yml logs -f

# Ejecutar migraciones
docker-compose -f dev.yml exec api python manage.py migrate

# Crear superusuario
docker-compose -f dev.yml exec api python manage.py createsuperuser

# Shell de Django
docker-compose -f dev.yml exec api python manage.py shell
```

### Celery

```bash
# Ver tareas en Flower
open http://localhost:5555

# Ver workers
docker-compose -f dev.yml logs celery_worker

# Ver beat (tareas programadas)
docker-compose -f dev.yml logs celery_beat
```

### Monitoreo

```bash
# Estado de servicios
docker-compose -f dev.yml ps

# Logs de todos los servicios
docker-compose -f dev.yml logs

# Logs de un servicio específico
docker-compose -f dev.yml logs api
```

## 🔒 Seguridad

### Autenticación

- Tokens de autenticación
- Verificación de usuarios
- Permisos granulares

### Validación de Datos

- Esquemas JSON para validación
- Validación de fuentes de cumplimiento
- Sanitización de datos

### Logs de Auditoría

- Logs de todas las actividades
- Logs de cumplimiento
- Logs de acceso

## 📝 API Endpoints

### Cumplimiento

- `GET /api/compliance/sources/` - Listar fuentes
- `POST /api/compliance/configs/` - Crear configuración
- `GET /api/compliance/data/` - Listar datos enviados

### Usuarios

- `GET /api/users/owners/` - Listar propietarios
- `POST /api/users/notifications/` - Configurar notificaciones

### Telemetría

- `GET /api/telemetry/data/` - Datos de telemetría
- `POST /api/telemetry/process/` - Procesar datos

## 🚨 Troubleshooting

### Problemas Comunes

1. **Error de conexión a Redis**

   ```bash
   docker-compose -f dev.yml restart redis
   ```

2. **Error de migraciones**

   ```bash
   docker-compose -f dev.yml exec api python manage.py migrate --run-syncdb
   ```

3. **Celery no procesa tareas**

   ```bash
   docker-compose -f dev.yml restart celery_worker
   ```

4. **MQTT no conecta**
   ```bash
   docker-compose -f dev.yml restart mqtt_broker
   ```

### Logs de Debug

```bash
# Ver logs detallados
docker-compose -f dev.yml logs -f --tail=100

# Ver logs de un servicio específico
docker-compose -f dev.yml logs -f api

# Ver logs de Celery
docker-compose -f dev.yml logs -f celery_worker
```

## 📞 Soporte

Para soporte técnico o preguntas sobre el sistema:

1. Revisar logs del sistema
2. Ejecutar script de verificación
3. Consultar documentación
4. Contactar al equipo de desarrollo

---

**Stack VPS** - Sistema Profesional de Telemetría y Cumplimiento
