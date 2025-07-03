# 🔄 Conversión de Pulsos a Volumen

## 📋 Resumen

El sistema ahora incluye **conversión automática de pulsos a volumen** para variables como `total` y `flow`. Los datos que llegan en pulsos se convierten automáticamente a unidades de volumen (m³, l/s).

## 🎯 Fórmula de Conversión

```python
# Pulsos → Litros → Metros Cúbicos
metros_cubicos = (pulsos × factor_calibración) / (pulsos_por_litro × 1000)

# Ejemplos:
# 1000 pulsos/litro: m³ = pulsos / 1,000,000
# 100 pulsos/litro:  m³ = pulsos / 100,000
# 500 pulsos/litro:  m³ = pulsos / 500,000
```

## 🚀 Configuración Rápida

### 1️⃣ Ejecutar Comando de Configuración

```bash
# Configurar todo el sistema
python manage.py setup_pulse_conversion

# Con prueba incluida
python manage.py setup_pulse_conversion --test

# Ver configuración actual
python manage.py setup_pulse_conversion --show-config
```

### 2️⃣ Configuración Manual

#### Variables

```python
from api.apps.variables.models import Variable

# Crear variable total con conversión de pulsos
total_var = Variable.objects.create(
    name="Totalizado de Agua",
    code="total",
    variable_type="TOTALIZADO",
    unit="CUBIC_METERS",
    processing_config={
        "rules": [
            {
                "type": "pulse_conversion",
                "pulses_per_liter": 1000,
                "target_unit": "m³"
            }
        ]
    }
)
```

#### Puntos de Captación

```python
from api.apps.catchment.models import CatchmentPoint

# Configurar punto con constantes de pulsos
point = CatchmentPoint.objects.get(id=1)
point.config.update({
    "pulse_constants": {
        "total": {
            "pulses_per_liter": 1000,
            "calibration_factor": 1.023,
            "description": "Contador total - 1000 pulsos por litro"
        },
        "flow": {
            "pulses_per_liter": 500,
            "calibration_factor": 1.015,
            "description": "Caudal instantáneo - 500 pulsos por litro"
        }
    }
})
point.save()
```

## 📊 Ejemplos de Uso

### Datos que Llegan

```json
{
  "device_id": "DEV001",
  "total": 1500, // PULSOS
  "flow": 15.5, // l/s
  "level": 2.3, // metros
  "temperature": 18.5 // °C
}
```

### Datos Procesados

```python
# Antes de la conversión
raw_total = 1500  # pulsos

# Después de la conversión
processed_total = 1500 / (1000 * 1000) * 1.023 = 0.0015345 m³
```

### Resultado Final

```python
{
  "total": 0.0015345,  # m³ (convertido de pulsos)
  "flow": 15.5,        # l/s (sin cambios)
  "level": 2.3,        # m (sin cambios)
  "temperature": 18.5  # °C (sin cambios)
}
```

## 🔧 Configuración por Punto

### Estructura de Configuración

```json
{
  "pulse_constants": {
    "total": {
      "pulses_per_liter": 1000,
      "calibration_factor": 1.023,
      "description": "Contador total - 1000 pulsos por litro"
    },
    "flow": {
      "pulses_per_liter": 500,
      "calibration_factor": 1.015,
      "description": "Caudal instantáneo - 500 pulsos por litro"
    }
  },
  "variables": ["total", "flow", "level", "temperature"],
  "alerts": {
    "level_critical": 95.0,
    "flow_minimum": 0.1
  }
}
```

### Parámetros de Conversión

| Parámetro            | Descripción                     | Valor por Defecto |
| -------------------- | ------------------------------- | ----------------- |
| `pulses_per_liter`   | Pulsos por litro del contador   | 1000              |
| `calibration_factor` | Factor de calibración           | 1.0               |
| `description`        | Descripción de la configuración | -                 |

## 🧪 Pruebas

### Script de Prueba

```python
from api.apps.telemetry.processors.processor import TelemetryProcessor
from api.apps.catchment.models import CatchmentPoint

# Obtener punto de captación
point = CatchmentPoint.objects.first()

# Crear procesador
processor = TelemetryProcessor()

# Datos de prueba
test_data = {
    "device_id": point.device_id,
    "total": 1500,      # PULSOS
    "flow": 15.5,       # l/s
    "level": 2.3,       # metros
}

# Procesar datos
result = processor.process_catchment_point_data(point, test_data)

print(f"Total: {test_data['total']} pulsos → {result.total:.6f} m³")
print(f"Flow: {test_data['flow']} l/s → {result.flow:.3f} l/s")
```

### Verificación Manual

```python
# Verificar conversión
pulses = 1500
pulses_per_liter = 1000
calibration_factor = 1.023

expected = pulses / (pulses_per_liter * 1000) * calibration_factor
print(f"Esperado: {expected:.6f} m³")
print(f"Obtenido: {result.total:.6f} m³")
```

## 🔍 Monitoreo

### Logs de Conversión

```python
# Los logs muestran las conversiones aplicadas
logger.info(f"Total convertido para punto {point.id}: 1500 pulsos → 0.001535 m³")
```

### Alertas de Conversión

```python
# Si hay errores en la conversión
processed_data.alerts.append("Error en conversión de pulsos: división por cero")
```

## 🚨 Casos Especiales

### Detección Automática de Pulsos

```python
# El sistema detecta automáticamente si flow viene en pulsos
if processed_data.flow > 100:  # Probablemente pulsos
    # Aplicar conversión
    processed_data.flow = processed_data.flow / pulses_per_liter
```

### Valores por Defecto

```python
# Si no hay configuración, usar valores por defecto
pulses_per_liter = config.get('pulses_per_liter', 1000)
calibration_factor = config.get('calibration_factor', 1.0)
```

## 📈 Rendimiento

### Optimización

- La conversión se aplica solo cuando es necesario
- Los valores se cachean para evitar recálculos
- El procesamiento es asíncrono con Celery

### Métricas

```python
# Métricas de conversión
conversion_metrics = {
    "total_conversions": 1500,
    "flow_conversions": 0,
    "errors": 0,
    "processing_time_ms": 2.5
}
```

## 🔄 Migración

### Desde Sistema Anterior

```python
# Los datos existentes se procesan automáticamente
# No es necesario migrar datos históricos
# La conversión se aplica solo a nuevos datos
```

### Configuración Gradual

```python
# Puedes configurar punto por punto
# Los puntos sin configuración usan valores por defecto
# No afecta el funcionamiento del sistema
```

## 📞 Soporte

### Comandos Útiles

```bash
# Ver configuración actual
python manage.py setup_pulse_conversion --show-config

# Probar conversión
python manage.py setup_pulse_conversion --test

# Script independiente
python scripts/setup_pulse_conversion.py
```

### Debugging

```python
# Activar logs detallados
import logging
logging.getLogger('api.apps.telemetry.processors').setLevel(logging.DEBUG)
```

---

## ✅ Resumen de Implementación

1. **✅ Procesador actualizado** con conversión automática
2. **✅ Script de configuración** para setup rápido
3. **✅ Comando Django** para gestión
4. **✅ Documentación completa** con ejemplos
5. **✅ Pruebas incluidas** para validación

La conversión de pulsos está **lista para usar** en producción. 🚀
