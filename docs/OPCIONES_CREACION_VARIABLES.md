# 🔧 Opciones de Creación de Variables y Reglas

## 📋 Análisis de la Estructura Actual

### **Relación Variables ↔ Puntos de Captación**

Actualmente, la relación entre variables y puntos de captación es **indirecta** a través de los puntos de datos:

```python
# Variable (independiente)
class Variable(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    variable_type = models.CharField(max_length=20, choices=VARIABLE_TYPES)
    # ... otros campos

# Punto de Captación (independiente)
class CatchmentPoint(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100, unique=True)
    device_id = models.CharField(max_length=100, unique=True)
    # ... otros campos

# Punto de Datos (conecta ambos)
class VariableDataPoint(models.Model):
    variable = models.ForeignKey(Variable, ...)
    catchment_point_id = models.IntegerField()  # Referencia indirecta
    value = models.DecimalField(...)
    timestamp = models.DateTimeField(...)
```

## 🎯 **Opciones de Creación de Variables**

### **Opción 1: Variables Independientes (Actual)**

```python
# Crear variable primero
variable = Variable.objects.create(
    name="Nivel de Agua",
    code="NIVEL_001",
    variable_type="NIVEL",
    unit="METERS"
)

# Luego crear puntos de datos que la referencien
data_point = VariableDataPoint.objects.create(
    variable=variable,
    catchment_point_id=123,
    value=15.5,
    timestamp=timezone.now()
)
```

**✅ Ventajas:**

- Variables reutilizables en múltiples puntos
- Configuración centralizada
- Fácil mantenimiento

**❌ Desventajas:**

- Relación indirecta
- No hay validación automática de existencia del punto
- Configuración separada

---

### **Opción 2: Variables Vinculadas a Puntos de Captación**

```python
# Modelo de relación directa
class CatchmentPointVariable(models.Model):
    catchment_point = models.ForeignKey(CatchmentPoint, ...)
    variable = models.ForeignKey(Variable, ...)
    is_active = models.BooleanField(default=True)
    config = models.JSONField(default=dict)

    class Meta:
        unique_together = ['catchment_point', 'variable']
```

**✅ Ventajas:**

- Relación explícita y validada
- Configuración específica por punto
- Fácil consulta de variables por punto

**❌ Desventajas:**

- Modelo adicional
- Más complejidad en la gestión

---

### **Opción 3: Variables Embebidas en Puntos de Captación**

```python
# Modificar CatchmentPoint para incluir variables
class CatchmentPoint(models.Model):
    # ... campos existentes

    # Variables configuradas
    configured_variables = models.JSONField(
        default=list,
        verbose_name=_('Variables configuradas'),
        help_text=_('Lista de variables configuradas para este punto')
    )
```

**✅ Ventajas:**

- Configuración simple
- Todo en un lugar
- Fácil de entender

**❌ Desventajas:**

- Menos flexibilidad
- Difícil reutilización
- Limitaciones de JSONField

---

### **Opción 4: Sistema Híbrido (Recomendado)**

```python
# Variables base (reutilizables)
class Variable(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    variable_type = models.CharField(max_length=20, choices=VARIABLE_TYPES)
    # ... configuración base

# Configuración específica por punto
class CatchmentPointVariableConfig(models.Model):
    catchment_point = models.ForeignKey(CatchmentPoint, ...)
    variable = models.ForeignKey(Variable, ...)

    # Configuración específica
    is_enabled = models.BooleanField(default=True)
    custom_config = models.JSONField(default=dict)
    alert_rules = models.JSONField(default=dict)

    class Meta:
        unique_together = ['catchment_point', 'variable']
```

## 🚀 **Opciones para Reglas de Variables**

### **Opción A: Reglas en el Modelo Variable**

```python
class Variable(models.Model):
    # ... campos existentes

    # Reglas globales
    validation_rules = models.JSONField(default=dict)
    alert_rules = models.JSONField(default=dict)
    processing_rules = models.JSONField(default=dict)
```

### **Opción B: Reglas en Configuración de Punto**

```python
class CatchmentPointVariableConfig(models.Model):
    # ... campos existentes

    # Reglas específicas por punto
    validation_rules = models.JSONField(default=dict)
    alert_rules = models.JSONField(default=dict)
    processing_rules = models.JSONField(default=dict)
```

### **Opción C: Sistema de Reglas Independiente**

```python
class VariableRule(models.Model):
    variable = models.ForeignKey(Variable, ...)
    rule_type = models.CharField(max_length=20, choices=[
        ('VALIDATION', 'Validación'),
        ('ALERT', 'Alerta'),
        ('PROCESSING', 'Procesamiento'),
    ])
    rule_config = models.JSONField()
    is_active = models.BooleanField(default=True)
```

## 📊 **Recomendación: Sistema Híbrido**

### **Estructura Propuesta:**

```python
# 1. Variables base (reutilizables)
class Variable(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    variable_type = models.CharField(max_length=20, choices=VARIABLE_TYPES)
    unit = models.CharField(max_length=20, choices=UNIT_TYPES)

    # Configuración base
    base_config = models.JSONField(default=dict)
    base_rules = models.JSONField(default=dict)

# 2. Configuración específica por punto
class CatchmentPointVariableConfig(models.Model):
    catchment_point = models.ForeignKey(CatchmentPoint, ...)
    variable = models.ForeignKey(Variable, ...)

    # Estado
    is_enabled = models.BooleanField(default=True)

    # Configuración específica
    custom_config = models.JSONField(default=dict)
    custom_rules = models.JSONField(default=dict)

    # Reglas de alerta
    alert_rules = models.JSONField(default=dict)

    class Meta:
        unique_together = ['catchment_point', 'variable']

# 3. Puntos de datos (sin cambios)
class VariableDataPoint(models.Model):
    variable = models.ForeignKey(Variable, ...)
    catchment_point_id = models.IntegerField()
    value = models.DecimalField(...)
    timestamp = models.DateTimeField(...)
```

### **Flujo de Creación:**

#### **Escenario 1: Crear Variable y Asignar a Punto Existente**

```python
# 1. Crear variable base
variable = Variable.objects.create(
    name="Nivel de Agua",
    code="NIVEL_001",
    variable_type="NIVEL",
    unit="METERS",
    base_config={
        "min_value": 0,
        "max_value": 100,
        "decimal_places": 2
    }
)

# 2. Configurar en punto específico
config = CatchmentPointVariableConfig.objects.create(
    catchment_point=catchment_point,
    variable=variable,
    custom_config={
        "level_position": 10.5,
        "alert_threshold": 80.0
    },
    alert_rules={
        "high_level": {"threshold": 80.0, "action": "email"},
        "low_level": {"threshold": 5.0, "action": "sms"}
    }
)
```

#### **Escenario 2: Crear Punto de Captación con Variables**

```python
# 1. Crear punto de captación
catchment_point = CatchmentPoint.objects.create(
    name="Pozo Principal",
    code="POZO_001",
    device_id="DEV_001"
)

# 2. Asignar variables existentes
variables_to_assign = [
    {"variable_code": "NIVEL_001", "custom_config": {...}},
    {"variable_code": "CAUDAL_001", "custom_config": {...}},
]

for var_config in variables_to_assign:
    variable = Variable.objects.get(code=var_config["variable_code"])
    CatchmentPointVariableConfig.objects.create(
        catchment_point=catchment_point,
        variable=variable,
        custom_config=var_config["custom_config"]
    )
```

## 🔧 **Implementación Recomendada**

### **Paso 1: Crear el Modelo de Configuración**

```python
# api/apps/variables/models/configs/catchment_point_variable_config.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from api.apps.core.models import BaseModel
from ...catchment.models.points.catchment_point import CatchmentPoint
from ..variables.variable import Variable

class CatchmentPointVariableConfig(BaseModel):
    """Configuración de variables por punto de captación"""

    catchment_point = models.ForeignKey(
        CatchmentPoint,
        on_delete=models.CASCADE,
        related_name='variable_configs',
        verbose_name=_('Punto de captación')
    )

    variable = models.ForeignKey(
        Variable,
        on_delete=models.CASCADE,
        related_name='catchment_configs',
        verbose_name=_('Variable')
    )

    # Configuración específica
    custom_config = models.JSONField(
        default=dict,
        verbose_name=_('Configuración personalizada')
    )

    # Reglas de alerta
    alert_rules = models.JSONField(
        default=dict,
        verbose_name=_('Reglas de alerta')
    )

    class Meta:
        verbose_name = _('Configuración Variable-Punto')
        verbose_name_plural = _('Configuraciones Variable-Punto')
        db_table = 'variables_catchment_point_variable_config'
        unique_together = ['catchment_point', 'variable']
```

### **Paso 2: Crear Serializers**

```python
# api/apps/variables/serializers/configs/catchment_point_variable_config.py
from rest_framework import serializers
from api.apps.variables.models.configs import CatchmentPointVariableConfig
from ...catchment.serializers.points.catchment_point import CatchmentPointSerializer
from ..variables.variable import VariableSerializer

class CatchmentPointVariableConfigSerializer(serializers.ModelSerializer):
    """Serializador para configuración variable-punto"""

    catchment_point = CatchmentPointSerializer(read_only=True)
    variable = VariableSerializer(read_only=True)

    class Meta:
        model = CatchmentPointVariableConfig
        fields = [
            'id', 'catchment_point', 'variable', 'custom_config',
            'alert_rules', 'is_active', 'created_at', 'updated_at'
        ]
```

### **Paso 3: Crear Vistas**

```python
# api/apps/variables/views/configs.py
from rest_framework import viewsets
from api.apps.variables.models.configs import CatchmentPointVariableConfig
from ..serializers.configs import CatchmentPointVariableConfigSerializer

class CatchmentPointVariableConfigViewSet(viewsets.ModelViewSet):
    """ViewSet para configuración variable-punto"""

    queryset = CatchmentPointVariableConfig.objects.all()
    serializer_class = CatchmentPointVariableConfigSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrar por punto de captación
        catchment_point_id = self.request.query_params.get('catchment_point_id')
        if catchment_point_id:
            queryset = queryset.filter(catchment_point_id=catchment_point_id)

        # Filtrar por variable
        variable_id = self.request.query_params.get('variable_id')
        if variable_id:
            queryset = queryset.filter(variable_id=variable_id)

        return queryset
```

## 📋 **Resumen de Opciones**

| Aspecto                   | Opción Actual | Opción Recomendada             |
| ------------------------- | ------------- | ------------------------------ |
| **Creación de Variables** | Independiente | Híbrida (base + configuración) |
| **Relación con Puntos**   | Indirecta     | Directa + configuración        |
| **Reglas**                | En Variable   | En configuración específica    |
| **Flexibilidad**          | Media         | Alta                           |
| **Mantenibilidad**        | Media         | Alta                           |
| **Reutilización**         | Alta          | Alta                           |

## 🎯 **Próximos Pasos**

1. **Implementar modelo de configuración**
2. **Crear serializers y vistas**
3. **Migrar datos existentes**
4. **Actualizar documentación**
5. **Probar funcionalidades**

¿Te gustaría que implemente alguna de estas opciones específicamente?
