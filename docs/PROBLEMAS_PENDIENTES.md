# Problemas Pendientes - Sistema de Telemetría

## 🚨 Problemas Críticos a Resolver

### 1. **Referencias Rotas en Telemetría**

**Archivos afectados**:

- `api/apps/telemetry/metrics.py`
- `api/apps/telemetry/views.py`
- `api/apps/telemetry/processor.py`
- `api/apps/telemetry/dga_processor.py`

**Problema**: Referencias a modelos que ya no existen o están en otras apps

**Solución**: Actualizar imports y referencias a los nuevos modelos

---

### 2. **Configuración de Apps Faltante**

**Archivo**: `api/config/settings/base.py`

**Problema**: Apps no están correctamente configuradas en `INSTALLED_APPS`

**Solución**: Verificar y corregir la configuración de apps

---

### 3. **URLs No Configuradas**

**Archivo**: `api/config/urls/main.py`

**Problema**: Se eliminó la referencia a `core.router` pero no se reemplazó

**Solución**: Configurar URLs para las nuevas apps

---

### 4. **Modelos Duplicados**

**Problema**: `TelemetryData` y `InteractionDetail` son similares

**Solución**: Decidir cuál mantener o cómo migrar

---

## 🔧 Acciones Requeridas

### ✅ **Completado**

- [x] Eliminar app `core`
- [x] Crear nuevos modelos de telemetría
- [x] Configurar admin de Django
- [x] Actualizar `AUTH_USER_MODEL`
- [x] Documentar estructura del sistema

### ⏳ **Pendiente**

- [ ] Arreglar imports en telemetría
- [ ] Configurar URLs principales
- [ ] Crear serializadores para nuevos modelos
- [ ] Adaptar vistas existentes
- [ ] Crear migraciones
- [ ] Probar sistema completo

---

## 📋 Plan de Acción

### **Fase 1: Arreglar Referencias**

1. Actualizar imports en `telemetry/metrics.py`
2. Actualizar imports en `telemetry/views.py`
3. Actualizar imports en `telemetry/processor.py`
4. Actualizar imports en `telemetry/dga_processor.py`

### **Fase 2: Configurar URLs**

1. Crear routers para cada app
2. Configurar URLs principales
3. Verificar endpoints

### **Fase 3: Crear Serializadores**

1. Serializadores para `RawTelemetryData`
2. Serializadores para `ProcessedTelemetryData`
3. Serializadores para `ResponseSchema`
4. Serializadores para `ProcessingConstant`

### **Fase 4: Migraciones**

1. Crear migraciones para nuevos modelos
2. Migrar datos existentes
3. Probar integridad

### **Fase 5: Testing**

1. Probar endpoints
2. Verificar admin
3. Probar procesamiento de datos

---

## 🎯 Estado Actual

**✅ Sistema Reorganizado**: Las apps están bien estructuradas
**✅ Modelos Creados**: Nuevos modelos de telemetría implementados
**✅ Admin Configurado**: Panel de administración listo
**❌ Referencias Rotas**: Necesitan arreglarse
**❌ URLs No Configuradas**: Faltan endpoints
**❌ Migraciones Pendientes**: No se han creado

---

## 🚀 Próximo Paso Inmediato

**Arreglar referencias en telemetría** para que el sistema pueda ejecutarse sin errores.

¿Procedemos con la Fase 1?
