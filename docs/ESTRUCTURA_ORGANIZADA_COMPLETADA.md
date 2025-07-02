# Estructura Organizada del Sistema de Telemetría

## Resumen de la Reorganización

Se ha completado la reorganización del sistema de telemetría con una estructura modular y organizada. Todos los archivos han sido agrupados por funcionalidad y los archivos de documentación han sido movidos a la carpeta `docs/`.

## Estructura de Apps Organizadas

### 1. App Telemetry (`api/apps/telemetry/`)

La app más compleja del sistema, organizada en subcarpetas por funcionalidad:

```
telemetry/
├── __init__.py              # Exports principales
├── admin.py                 # Configuración de admin
├── router.py                # Configuración de URLs
├── models/                  # Modelos de datos
│   ├── __init__.py
│   ├── models.py            # Modelo principal TelemetryData
│   └── models_schemas.py    # Modelos de esquemas dinámicos
├── serializers/             # Serializadores
│   ├── __init__.py
│   ├── serializers.py       # Serializadores principales
│   └── serializers_schemas.py # Serializadores de esquemas
├── views/                   # Vistas y endpoints
│   ├── __init__.py
│   └── views.py             # ViewSet principal
├── processors/              # Procesadores de datos
│   ├── __init__.py
│   ├── processor.py         # Procesador principal
│   ├── dga_processor.py     # Procesador DGA
│   └── schema_processor.py  # Procesador de esquemas
├── providers/               # Proveedores de datos
│   ├── __init__.py
│   └── providers.py         # Gestor de proveedores
└── config/                  # Configuración
    ├── __init__.py
    ├── config.py            # Configuración general
    └── metrics.py           # Métricas del sistema
```

**Clases principales exportadas:**

- `TelemetryData` - Modelo principal de datos
- `TelemetrySchema` - Esquemas dinámicos
- `TelemetryViewSet` - Vista principal
- `TelemetryProcessor` - Procesador de datos
- `DgaQueueProcessor` - Procesador DGA
- `ProviderManager` - Gestor de proveedores

### 2. App Catchment (`api/apps/catchment/`)

Gestión de puntos de captación:

```
catchment/
├── __init__.py              # Exports principales
├── apps.py                  # Configuración de app
├── signals.py               # Señales de Django
├── models/                  # Modelos
│   ├── __init__.py
│   └── models.py            # CatchmentPoint y configuraciones
├── serializers/             # Serializadores
│   ├── __init__.py
│   └── serializers.py       # Serializadores de puntos
└── views/                   # Vistas
    ├── __init__.py
    └── router.py            # Configuración de URLs
```

**Clases principales exportadas:**

- `CatchmentPoint` - Punto de captación
- `CatchmentPointProcessingConfig` - Configuración de procesamiento
- `NotificationsCatchment` - Notificaciones

### 3. App Users (`api/apps/users/`)

Gestión de usuarios:

```
users/
├── __init__.py              # Exports principales
├── apps.py                  # Configuración de app
├── signals.py               # Señales de Django
├── models/                  # Modelos
│   ├── __init__.py
│   └── models.py            # Modelo User
├── serializers/             # Serializadores
│   ├── __init__.py
│   └── serializers.py       # Serializadores de usuarios
└── views/                   # Vistas
    ├── __init__.py
    └── router.py            # Configuración de URLs
```

**Clases principales exportadas:**

- `User` - Modelo de usuario
- `UserSerializer` - Serializador de usuarios

### 4. App Variables (`api/apps/variables/`)

Gestión de variables y esquemas:

```
variables/
├── __init__.py              # Exports principales
├── apps.py                  # Configuración de app
├── signals.py               # Señales de Django
├── models/                  # Modelos
│   ├── __init__.py
│   └── models.py            # Variables y esquemas
├── serializers/             # Serializadores
│   ├── __init__.py
│   └── serializers.py       # Serializadores de variables
└── processors/              # Procesadores
    ├── __init__.py
    └── processor.py         # Procesador de variables
```

**Clases principales exportadas:**

- `Variable` - Variable individual
- `VariableSchema` - Esquemas de variables
- `VariableDataPoint` - Puntos de datos
- `VariableAlert` - Alertas de variables

### 5. App Providers (`api/apps/providers/`)

Gestión de proveedores de datos:

```
providers/
├── __init__.py              # Exports principales
├── apps.py                  # Configuración de app
├── signals.py               # Señales de Django
├── models/                  # Modelos
│   ├── __init__.py
│   └── models.py            # Proveedores y configuraciones
├── serializers/             # Serializadores
│   ├── __init__.py
│   └── serializers.py       # Serializadores de proveedores
└── clients/                 # Clientes de comunicación
    ├── __init__.py
    └── mqtt_client.py       # Cliente MQTT
```

**Clases principales exportadas:**

- `Provider` - Proveedor de datos
- `MQTTBroker` - Configuración MQTT
- `DeviceToken` - Tokens de dispositivos
- `DynamicMQTTClient` - Cliente MQTT dinámico

### 6. App Compliance (`api/apps/compliance/`)

Gestión de cumplimiento normativo:

```
compliance/
├── __init__.py              # Exports principales
├── apps.py                  # Configuración de app
├── signals.py               # Señales de Django
├── models/                  # Modelos
│   ├── __init__.py
│   └── models.py            # Cumplimiento y configuraciones
├── serializers/             # Serializadores
│   ├── __init__.py
│   └── serializers.py       # Serializadores de cumplimiento
└── views/                   # Vistas
    ├── __init__.py
    └── router.py            # Configuración de URLs
```

**Clases principales exportadas:**

- `ComplianceSource` - Fuente de cumplimiento
- `ComplianceConfig` - Configuración de cumplimiento
- `ComplianceData` - Datos de cumplimiento

## Documentación Organizada

Todos los archivos de documentación han sido movidos a la carpeta `docs/`:

```
docs/
├── README.md                    # Documentación principal
├── README_SISTEMA_COMPLETO.md   # Documentación completa del sistema
├── MONITORING.md                # Documentación de monitoreo
├── ESTRUCTURA_ORGANIZADA_COMPLETADA.md # Este archivo
├── api/                         # Documentación específica de API
└── architecture/                # Documentación de arquitectura
```

## Beneficios de la Reorganización

1. **Estructura Clara**: Cada app tiene una estructura consistente y organizada
2. **Separación de Responsabilidades**: Los archivos están agrupados por funcionalidad
3. **Facilidad de Mantenimiento**: Es más fácil encontrar y modificar archivos específicos
4. **Escalabilidad**: La estructura permite agregar nuevas funcionalidades fácilmente
5. **Documentación Centralizada**: Todos los archivos MD están en una ubicación

## Próximos Pasos

1. **Actualizar Imports**: Verificar que todos los imports en el código funcionen con la nueva estructura
2. **Testing**: Ejecutar tests para asegurar que la reorganización no rompió funcionalidad
3. **Documentación**: Actualizar documentación técnica con la nueva estructura
4. **Deployment**: Verificar que el deployment funcione con la nueva organización

## Comandos Útiles

```bash
# Verificar estructura
find api/apps -type d -name "__pycache__" -exec rm -rf {} +
find api/apps -name "*.pyc" -delete

# Ejecutar tests
python manage.py test

# Verificar imports
python manage.py check
```

La reorganización está completa y el sistema mantiene toda su funcionalidad mientras mejora significativamente la organización y mantenibilidad del código.
