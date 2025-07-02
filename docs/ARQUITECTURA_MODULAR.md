# Arquitectura Modular para Telemetría

## Visión General

El sistema está diseñado con una arquitectura modular que permite separar los servicios en diferentes máquinas según las necesidades de escalabilidad y mantenimiento.

## Módulos Principales

### 1. Core (Núcleo)

**Responsabilidades:**

- Modelos base del sistema
- Configuraciones globales
- Utilidades comunes
- Autenticación básica

**Servicios:**

- Gestión de usuarios básica
- Configuraciones del sistema
- Logs centralizados

**Separación:** Puede ejecutarse en la misma máquina que otros servicios o como servicio independiente.

### 2. Telemetry (Telemetría)

**Responsabilidades:**

- Recolección de datos de proveedores
- Procesamiento de datos
- Almacenamiento de datos de telemetría
- Validaciones y alertas

**Servicios:**

- API de datos de telemetría
- Procesamiento inteligente de datos
- Monitoreo de dispositivos
- Alertas en tiempo real

**Separación:** Servicio crítico que puede ejecutarse en máquinas dedicadas para alta disponibilidad.

### 3. Compliance (Cumplimiento)

**Responsabilidades:**

- Gestión de normativas (DGA, SMA, etc.)
- Envío de datos a entidades reguladoras
- Validación de cumplimiento
- Logs de cumplimiento

**Servicios:**

- API de cumplimiento
- Procesamiento de normativas
- Envío automático de datos
- Reportes de cumplimiento

**Separación:** Puede ejecutarse en máquinas separadas para cumplir requisitos de seguridad específicos.

### 4. Catchment (Puntos de Captación)

**Responsabilidades:**

- Gestión de puntos de captación
- Configuraciones de dispositivos
- Metadatos de ubicación

**Servicios:**

- API de puntos de captación
- Gestión de configuraciones
- Información geográfica

**Separación:** Servicio ligero que puede compartir máquina con otros servicios.

### 5. Users (Usuarios)

**Responsabilidades:**

- Gestión de usuarios
- Autenticación y autorización
- Perfiles de usuario

**Servicios:**

- API de usuarios
- Gestión de sesiones
- Notificaciones de usuario

**Separación:** Puede ejecutarse como servicio independiente para centralizar la gestión de usuarios.

## Configuración de Separación

### Escenario 1: Monolítico (Desarrollo)

```
Máquina Única:
├── Core
├── Telemetry
├── Compliance
├── Catchment
└── Users
```

### Escenario 2: Separación Básica (Producción)

```
Máquina 1 - API Principal:
├── Core
├── Catchment
└── Users

Máquina 2 - Telemetría:
└── Telemetry

Máquina 3 - Cumplimiento:
└── Compliance
```

### Escenario 3: Alta Disponibilidad

```
Máquina 1 - Load Balancer:
└── Nginx/HAProxy

Máquina 2 - API Principal:
├── Core
├── Catchment
└── Users

Máquina 3 - Telemetría Principal:
└── Telemetry

Máquina 4 - Telemetría Secundaria:
└── Telemetry (réplica)

Máquina 5 - Cumplimiento:
└── Compliance

Máquina 6 - Base de Datos:
└── PostgreSQL
```

## Configuración de Docker

### docker-compose.yml Base

```yaml
version: "3.8"

services:
  # Core y servicios básicos
  api-core:
    build: ./api
    environment:
      - DJANGO_SETTINGS_MODULE=api.config.settings.production
      - SERVICE_TYPE=core
    volumes:
      - ./api:/app
    depends_on:
      - postgres
      - redis

  # Telemetría
  api-telemetry:
    build: ./api
    environment:
      - DJANGO_SETTINGS_MODULE=api.config.settings.production
      - SERVICE_TYPE=telemetry
    volumes:
      - ./api:/app
    depends_on:
      - postgres
      - redis

  # Cumplimiento
  api-compliance:
    build: ./api
    environment:
      - DJANGO_SETTINGS_MODULE=api.config.settings.production
      - SERVICE_TYPE=compliance
    volumes:
      - ./api:/app
    depends_on:
      - postgres
      - redis

  # Base de datos
  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB=telemetry
      - POSTGRES_USER=telemetry
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  # Cache
  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Variables de Entorno por Servicio

#### Core

```bash
SERVICE_TYPE=core
DJANGO_APPS=core,users,catchment
```

#### Telemetry

```bash
SERVICE_TYPE=telemetry
DJANGO_APPS=core,telemetry
TELEMETRY_ENABLED=true
PROCESSING_ENABLED=true
```

#### Compliance

```bash
SERVICE_TYPE=compliance
DJANGO_APPS=core,compliance
COMPLIANCE_ENABLED=true
DGA_ENABLED=true
```

## Configuración de Django

### settings/base.py

```python
import os

# Determinar qué apps cargar según el tipo de servicio
SERVICE_TYPE = os.environ.get('SERVICE_TYPE', 'core')

# Apps base que siempre se cargan
BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Apps específicas por servicio
SERVICE_APPS = {
    'core': [
        'api.apps.core',
        'api.apps.users',
        'api.apps.catchment',
    ],
    'telemetry': [
        'api.apps.core',
        'api.apps.telemetry',
    ],
    'compliance': [
        'api.apps.core',
        'api.apps.compliance',
    ],
}

# Cargar apps según el tipo de servicio
INSTALLED_APPS = BASE_APPS + SERVICE_APPS.get(SERVICE_TYPE, SERVICE_APPS['core'])
```

## Comunicación Entre Servicios

### API REST

Los servicios se comunican mediante APIs REST estándar:

- **Core API:** `http://core-service:8000/api/core/`
- **Telemetry API:** `http://telemetry-service:8001/api/telemetry/`
- **Compliance API:** `http://compliance-service:8002/api/compliance/`

### Base de Datos Compartida

Todos los servicios comparten la misma base de datos PostgreSQL para mantener consistencia de datos.

### Cache Compartido

Redis se usa como cache compartido para:

- Sesiones de usuario
- Datos de telemetría en caché
- Configuraciones de cumplimiento

## Monitoreo y Logs

### Logs Centralizados

Cada servicio envía logs a un sistema centralizado (ELK Stack o similar):

```python
# settings/logging.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/telemetry/app.log',
            'formatter': 'verbose',
        },
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'address': ('log-server', 514),
        },
    },
    'root': {
        'handlers': ['file', 'syslog'],
        'level': 'INFO',
    },
}
```

### Métricas

Cada servicio expone métricas en formato Prometheus:

- **Core:** Métricas de usuarios y sesiones
- **Telemetry:** Métricas de procesamiento y dispositivos
- **Compliance:** Métricas de envíos y cumplimiento

## Seguridad

### Autenticación Centralizada

Todos los servicios usan el mismo sistema de autenticación basado en JWT.

### Autorización por Servicio

Cada servicio maneja su propia autorización basada en roles y permisos.

### Comunicación Segura

Los servicios se comunican mediante HTTPS y autenticación mutua.

## Escalabilidad

### Horizontal

- Cada servicio puede escalar independientemente
- Load balancer distribuye la carga
- Base de datos con réplicas de lectura

### Vertical

- Cada máquina puede tener recursos específicos según el servicio
- Telemetría: CPU y memoria para procesamiento
- Compliance: Ancho de banda para envíos
- Core: Almacenamiento para logs

## Migración y Despliegue

### Migración Gradual

1. Desplegar servicios en modo monolítico
2. Separar servicios uno por uno
3. Configurar comunicación entre servicios
4. Optimizar recursos por servicio

### Rollback

Cada servicio puede volver a modo monolítico independientemente si es necesario.

## Beneficios de la Arquitectura Modular

1. **Escalabilidad:** Cada servicio puede escalar independientemente
2. **Mantenimiento:** Actualizaciones sin afectar todo el sistema
3. **Seguridad:** Aislamiento de servicios críticos
4. **Recursos:** Optimización de recursos por servicio
5. **Desarrollo:** Equipos pueden trabajar en servicios diferentes
6. **Resiliencia:** Fallos aislados no afectan todo el sistema
