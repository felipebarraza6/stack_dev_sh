# Estructura del Sistema de Telemetría - Organizada

## 📋 Resumen del Sistema

Este es un sistema de telemetría para monitoreo de recursos hídricos que incluye:

- **Captación de datos** desde dispositivos IoT
- **Procesamiento** con esquemas configurables
- **Almacenamiento** de datos brutos y procesados
- **Gestión de usuarios** y permisos
- **Cumplimiento regulatorio** (DGA)
- **Notificaciones** y alertas

## 🏗️ Arquitectura de Apps

### 1. **users** - Gestión de Usuarios

**Propósito**: Gestión de usuarios, autenticación y permisos

**Modelos principales**:

- `User` - Usuario del sistema (extiende AbstractUser)
- Campos: email, phone, company, notificaciones

**Responsabilidades**:

- Autenticación y autorización
- Gestión de perfiles de usuario
- Configuración de notificaciones

---

### 2. **catchment** - Puntos de Captación

**Propósito**: Gestión de puntos de monitoreo y configuración

**Modelos principales**:

- `CatchmentPoint` - Punto de captación de datos
- `CatchmentPointProcessingConfig` - Configuración de procesamiento
- `NotificationsCatchment` - Notificaciones del punto

**Responsabilidades**:

- Definición de puntos de monitoreo
- Configuración de dispositivos
- Gestión de ubicaciones y estados
- Configuración de procesamiento específica

---

### 3. **providers** - Proveedores de Datos

**Propósito**: Integración con proveedores de datos IoT

**Modelos principales**:

- `Provider` - Proveedor de datos (Twin, Nettra, etc.)
- `ProviderConfig` - Configuración del proveedor
- `ProviderToken` - Tokens de autenticación

**Responsabilidades**:

- Conexión con proveedores IoT
- Gestión de credenciales
- Configuración de endpoints

---

### 4. **telemetry** - Procesamiento de Telemetría ⭐

**Propósito**: Procesamiento y almacenamiento de datos de telemetría

**Modelos principales**:

- `TelemetryData` - Datos de telemetría (modelo legacy)
- `RawTelemetryData` - Datos brutos sin procesar
- `ProcessedTelemetryData` - Datos procesados según esquemas
- `ResponseSchema` - Esquemas de respuesta configurables
- `ProcessingConstant` - Constantes con fechas de vigencia
- `TelemetryNotification` - Notificaciones de telemetría
- `TelemetryProcessingLog` - Logs de procesamiento

**Responsabilidades**:

- Almacenamiento de datos brutos
- Procesamiento según esquemas configurables
- Aplicación de constantes con vigencia temporal
- Gestión de logs y notificaciones
- Integración con DGA

---

### 5. **variables** - Gestión de Variables

**Propósito**: Definición y configuración de variables de telemetría

**Modelos principales**:

- `Variable` - Variable individual
- `VariableSchema` - Esquemas de variables
- `VariableSchemaMapping` - Mapeo entre esquemas y variables
- `VariableProcessingRule` - Reglas de procesamiento
- `VariableDataPoint` - Puntos de datos de variables
- `VariableAlert` - Alertas de variables

**Responsabilidades**:

- Definición de tipos de variables
- Configuración de esquemas
- Reglas de procesamiento
- Sistema de alertas

---

### 6. **compliance** - Cumplimiento Regulatorio

**Propósito**: Gestión de cumplimiento con regulaciones (DGA)

**Modelos principales**:

- Modelos específicos para cumplimiento regulatorio
- Configuración de reportes
- Validación de datos

**Responsabilidades**:

- Cumplimiento con regulaciones
- Generación de reportes
- Validación de datos regulatorios

---

## 🔄 Flujo de Datos

```
1. Dispositivo IoT → 2. Provider → 3. RawTelemetryData → 4. ProcessedTelemetryData → 5. API Response
```

### Detalle del flujo:

1. **Captación**: Dispositivo envía datos al proveedor
2. **Recepción**: Provider recibe y valida datos
3. **Almacenamiento Bruto**: Se guarda en `RawTelemetryData`
4. **Procesamiento**: Se aplican esquemas y constantes
5. **Almacenamiento Procesado**: Se guarda en `ProcessedTelemetryData`
6. **Respuesta API**: Se devuelve según esquema solicitado

## 🎯 Ventajas del Sistema Mejorado

### ✅ **Flexibilidad**

- Esquemas de respuesta configurables
- Constantes con fechas de vigencia
- Almacenamiento de datos brutos

### ✅ **Integridad Histórica**

- Datos brutos preservados
- Constantes respetan fechas de vigencia
- No se adulteran registros históricos

### ✅ **Escalabilidad**

- Procesamiento modular
- Esquemas reutilizables
- Configuración por punto

### ✅ **Mantenibilidad**

- Apps especializadas
- Responsabilidades claras
- Código organizado

## 🚀 Próximos Pasos

1. **Migrar datos existentes** a nueva estructura
2. **Crear esquemas de respuesta** predefinidos
3. **Configurar constantes** de procesamiento
4. **Adaptar vistas y serializadores** al nuevo sistema
5. **Implementar lógica de procesamiento** con esquemas

## 📊 Comparación: Antes vs Después

| Aspecto        | Antes          | Después                   |
| -------------- | -------------- | ------------------------- |
| Almacenamiento | Tabla estática | Datos brutos + procesados |
| Esquemas       | Fijos          | Configurables             |
| Constantes     | Globales       | Con fechas de vigencia    |
| Flexibilidad   | Limitada       | Alta                      |
| Integridad     | Comprometida   | Preservada                |
| Mantenimiento  | Complejo       | Simple                    |

---

**Estado**: ✅ Sistema reorganizado y listo para migración
**Próximo**: Crear migraciones y adaptar código existente
