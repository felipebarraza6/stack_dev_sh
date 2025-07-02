# 🔍 Diagnóstico de la API - Stack VPS

## 📊 Estado Actual

### ❌ Problemas Identificados

1. **Archivos de configuración duplicados**:

   - `settings.py` (actual)
   - `settings_modular.py` (obsoleto)
   - `settings_improved.py` (obsoleto)

2. **Estructura confusa**:

   - `core/` contiene modelos que deberían estar en apps específicas
   - `old/` con código obsoleto
   - `cronjobs/` que debería ser reemplazado por Celery

3. **Separación incorrecta**:
   - Apps mezcladas con servicios
   - Lógica de negocio dispersa
   - Modelos duplicados

## 🏗️ Propuesta de Reorganización

### 📁 Estructura Propuesta

```
api/
├── apps/                   # Aplicaciones Django
│   ├── core/              # Funcionalidades centrales
│   ├── users/             # Gestión de usuarios
│   ├── providers/         # Proveedores de datos
│   ├── variables/         # Procesamiento de variables
│   ├── catchment/         # Puntos de captación
│   ├── compliance/        # Cumplimiento regulatorio
│   └── telemetry/         # Procesamiento de telemetría
├── services/              # Servicios de negocio
│   ├── telemetry/         # Servicios de telemetría
│   ├── compliance/        # Servicios de cumplimiento
│   ├── notifications/     # Servicios de notificaciones
│   └── data_processing/   # Procesamiento de datos
├── tasks/                 # Tareas Celery
├── utils/                 # Utilidades comunes
├── config/                # Configuraciones
│   ├── settings/          # Configuraciones por entorno
│   ├── urls/              # URLs organizadas
│   └── celery.py          # Configuración Celery
└── management/            # Comandos de gestión
```

### 🎯 Separación Apps vs Servicios

#### **Apps (Django Apps)**

- **Responsabilidad**: Modelos, vistas, serializers, admin
- **Propósito**: Gestión de datos y endpoints REST
- **Ejemplo**: `apps.users` maneja usuarios, `apps.catchment` maneja puntos de captación

#### **Servicios (Business Logic)**

- **Responsabilidad**: Lógica de negocio, procesamiento, integraciones
- **Propósito**: Operaciones complejas y reglas de negocio
- **Ejemplo**: `services.telemetry` procesa datos, `services.compliance` envía reportes

## 🔧 Plan de Reorganización

### Fase 1: Limpieza

1. Eliminar archivos obsoletos
2. Mover código de `old/` a servicios apropiados
3. Eliminar `cronjobs/` (reemplazado por Celery)

### Fase 2: Reorganización

1. Crear estructura `apps/` y `services/`
2. Mover modelos a apps correspondientes
3. Extraer lógica de negocio a servicios

### Fase 3: Configuración

1. Organizar configuraciones por entorno
2. Separar URLs por app
3. Configurar Celery correctamente

## 📋 Análisis Detallado por App

### Core (Actual)

**Problemas**:

- Contiene modelos que no son "core"
- Mezcla responsabilidades
- Tiene lógica de negocio

**Solución**:

- Mantener solo funcionalidades realmente centrales
- Mover modelos específicos a apps correspondientes

### Users

**Estado**: ✅ Bien organizado
**Acciones**: Mover a `apps/users`

### Providers

**Estado**: ✅ Bien organizado
**Acciones**: Mover a `apps/providers`

### Variables

**Estado**: ✅ Bien organizado
**Acciones**: Mover a `apps/variables`

### Catchment

**Estado**: ✅ Bien organizado
**Acciones**: Mover a `apps/catchment`

### Compliance

**Estado**: ✅ Bien organizado
**Acciones**: Mover a `apps/compliance`

### Telemetry

**Estado**: ⚠️ Necesita reorganización
**Acciones**: Separar en app y servicios

## 🚀 Próximos Pasos

1. **Crear nueva estructura de directorios**
2. **Mover apps existentes**
3. **Extraer servicios de lógica de negocio**
4. **Reorganizar configuraciones**
5. **Actualizar imports y referencias**
6. **Eliminar código obsoleto**

---

**¿Procedo con la reorganización completa?**
