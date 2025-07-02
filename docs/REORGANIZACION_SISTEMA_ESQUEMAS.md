# Reorganización del Sistema: Basado en Esquemas Dinámicos 🎯

## Problema Identificado

El sistema actual tiene un modelo `TelemetryData` rígido con campos fijos:

- `flow`, `total`, `level`, `water_table`, etc.
- No es flexible para diferentes tipos de dispositivos
- No aprovecha los esquemas de variables existentes
- Almacenamiento no optimizado

## Solución Propuesta: Sistema Basado en Esquemas

### 🏗️ **Nueva Arquitectura**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Raw Data      │───▶│ Variable Points │───▶│ Schema Groups   │
│   (JSON)        │    │   (Unitario)    │    │   (Dinámico)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 📊 **Flujo de Datos**

1. **Datos Brutos** → `RawTelemetryData` (JSON flexible)
2. **Procesamiento** → `VariableDataPoint` (un punto por variable)
3. **Agrupación** → Según esquemas dinámicos
4. **Consulta** → Agrupado por esquemas

## Estructura de Modelos

### 1. **Almacenamiento Unitario** (Ya existe)

```python
# api/apps/variables/models.py - VariableDataPoint
class VariableDataPoint(models.Model):
    variable = models.ForeignKey(Variable)
    catchment_point_id = models.IntegerField()
    value = models.DecimalField()
    timestamp = models.DateTimeField()
    quality = models.CharField()
    metadata = models.JSONField()
```

### 2. **Esquemas de Agrupación** (Nuevo)

```python
# api/apps/telemetry/models.py - TelemetrySchema
class TelemetrySchema(models.Model):
    name = models.CharField()
    description = models.TextField()
    schema_type = models.CharField()  # MEASUREMENT, DASHBOARD, REPORT
    variables = models.ManyToManyField(Variable)
    grouping_config = models.JSONField()
    display_config = models.JSONField()
```

### 3. **Datos Agrupados** (Nuevo)

```python
# api/apps/telemetry/models.py - TelemetryGroup
class TelemetryGroup(models.Model):
    schema = models.ForeignKey(TelemetrySchema)
    catchment_point = models.ForeignKey(CatchmentPoint)
    timestamp = models.DateTimeField()
    grouped_data = models.JSONField()  # Datos agrupados según esquema
    calculated_fields = models.JSONField()  # Campos calculados
```

## Ventajas del Nuevo Sistema

### ✅ **Flexibilidad Total**

- Cualquier variable puede ser almacenada
- Esquemas configurables sin cambios de código
- Soporte para nuevos tipos de dispositivos

### ✅ **Almacenamiento Optimizado**

- Un registro por variable por timestamp
- Índices optimizados para consultas
- Menor redundancia de datos

### ✅ **Agrupación Dinámica**

- Múltiples esquemas de visualización
- Agrupación en tiempo real
- Configuración sin migraciones

### ✅ **Escalabilidad**

- Fácil agregar nuevas variables
- Consultas eficientes por esquema
- Soporte para big data

## Ejemplo de Uso

### **1. Definir Esquema**

```json
{
  "name": "Medición Básica",
  "variables": ["flow", "level", "temperature"],
  "grouping_config": {
    "time_window": "1_hour",
    "aggregation": "average"
  }
}
```

### **2. Almacenar Datos**

```python
# Cada variable se almacena por separado
VariableDataPoint.objects.create(
    variable=flow_variable,
    catchment_point_id=1,
    value=15.5,
    timestamp=now()
)

VariableDataPoint.objects.create(
    variable=level_variable,
    catchment_point_id=1,
    value=2.3,
    timestamp=now()
)
```

### **3. Consultar Agrupado**

```python
# Se agrupan según el esquema
schema = TelemetrySchema.objects.get(name="Medición Básica")
grouped_data = TelemetryGroup.objects.filter(
    schema=schema,
    catchment_point_id=1,
    timestamp__date=today()
)
```

## Migración Propuesta

### **Fase 1: Preparación**

1. Crear nuevos modelos de esquemas
2. Migrar datos existentes a `VariableDataPoint`
3. Crear esquemas para datos existentes

### **Fase 2: Transición**

1. Actualizar procesadores para usar nuevo sistema
2. Mantener compatibilidad con API existente
3. Migrar vistas y serializadores

### **Fase 3: Optimización**

1. Eliminar `TelemetryData` obsoleto
2. Optimizar consultas y índices
3. Implementar caché por esquemas

## Beneficios Inmediatos

### 🚀 **Desarrollo**

- Menos código para mantener
- Más fácil agregar nuevas variables
- Testing más simple

### 🚀 **Operación**

- Consultas más rápidas
- Menor uso de almacenamiento
- Mejor monitoreo

### 🚀 **Flexibilidad**

- Esquemas configurables
- Soporte para cualquier dispositivo
- Agrupación dinámica

## Próximos Pasos

1. **Crear modelos de esquemas**
2. **Migrar datos existentes**
3. **Actualizar procesadores**
4. **Crear nuevos serializadores**
5. **Implementar vistas dinámicas**

¿Procedemos con esta reorganización? 🎯
