# Modelos Base Abstractos

## 📋 Descripción

Los modelos base abstractos son una excelente práctica en Django que permite reutilizar campos y funcionalidades comunes en múltiples modelos. Esto reduce la duplicación de código y mantiene consistencia en toda la aplicación.

## 🏗️ Estructura de Modelos Base

### 1. BaseModel

Modelo base con campos de auditoría comunes:

```python
from api.apps.core.models import BaseModel

class MiModelo(BaseModel):
    nombre = models.CharField(max_length=100)
    # Hereda automáticamente:
    # - created_at (DateTimeField, auto_now_add=True)
    # - updated_at (DateTimeField, auto_now=True)
    # - is_active (BooleanField, default=True)
```

**Campos heredados:**

- `created_at`: Fecha y hora de creación
- `updated_at`: Fecha y hora de última actualización
- `is_active`: Estado activo del registro

**Métodos heredados:**

- `is_recent`: Verifica si fue creado en las últimas 24 horas
- `age_days`: Retorna la edad del registro en días

### 2. TimestampedModel

Extiende BaseModel con timestamps específicos:

```python
from api.apps.core.models import TimestampedModel

class MiMedicion(TimestampedModel):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    # Hereda de BaseModel +:
    # - timestamp (DateTimeField)
    # - device_timestamp (DateTimeField, null=True)
```

**Campos adicionales:**

- `timestamp`: Timestamp del evento/medición
- `device_timestamp`: Timestamp reportado por el dispositivo

**Métodos adicionales:**

- `time_difference`: Diferencia entre timestamps del sistema y dispositivo

### 3. SoftDeleteModel

Extiende BaseModel con funcionalidad de soft delete:

```python
from api.apps.core.models import SoftDeleteModel

class MiDocumento(SoftDeleteModel):
    titulo = models.CharField(max_length=200)
    # Hereda de BaseModel +:
    # - deleted_at (DateTimeField, null=True)
    # - deleted_by (ForeignKey a User, null=True)
```

**Campos adicionales:**

- `deleted_at`: Fecha de eliminación (soft delete)
- `deleted_by`: Usuario que realizó la eliminación

**Métodos adicionales:**

- `is_deleted`: Verifica si está marcado como eliminado
- `soft_delete(user)`: Marca como eliminado sin borrar físicamente
- `restore()`: Restaura un registro eliminado
- `hard_delete()`: Elimina físicamente el registro

## 🔄 Migración de Modelos Existentes

### Script de Análisis

Ejecuta el script para identificar modelos que pueden migrar:

```bash
python scripts/migrate_to_base_models.py
```

### Proceso de Migración

1. **Identificar el modelo a migrar:**

   ```python
   # Antes
   class VariableAlert(models.Model):
       name = models.CharField(max_length=100)
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
       is_active = models.BooleanField(default=True)
   ```

2. **Actualizar imports:**

   ```python
   from api.apps.core.models import BaseModel
   ```

3. **Cambiar herencia:**

   ```python
   class VariableAlert(BaseModel):
       name = models.CharField(max_length=100)
       # Eliminar campos duplicados
   ```

4. **Eliminar campos duplicados:**
   - `created_at`
   - `updated_at`
   - `is_active`

## 📊 Beneficios

### ✅ Ventajas

- **DRY (Don't Repeat Yourself)**: No repetir código
- **Consistencia**: Comportamiento uniforme
- **Mantenibilidad**: Cambios centralizados
- **Funcionalidades**: Métodos útiles automáticos
- **Auditoría**: Trazabilidad completa

### ⚠️ Consideraciones

- **Migraciones**: Requiere migraciones de Django
- **Compatibilidad**: Verificar que no haya conflictos
- **Testing**: Probar funcionalidades heredadas

## 🎯 Casos de Uso

### Configuraciones

```python
class ProcessingConfig(BaseModel):
    name = models.CharField(max_length=100)
    config = models.JSONField()
    # Automáticamente tiene auditoría completa
```

### Mediciones/Telemetría

```python
class TelemetryData(TimestampedModel):
    value = models.DecimalField(max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=20)
    # Timestamps específicos para mediciones
```

### Documentos/Archivos

```python
class Document(SoftDeleteModel):
    title = models.CharField(max_length=200)
    file_path = models.CharField(max_length=500)
    # Soft delete para preservar historial
```

## 🔧 Configuración

### Agregar la app core

En `settings.py`:

```python
INSTALLED_APPS = [
    # ... otras apps
    'api.apps.core',
    # ... resto de apps
]
```

### Migraciones

Después de crear o modificar modelos base:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 📝 Ejemplos Prácticos

### Modelo con múltiples características

```python
class Event(TimestampedModel, SoftDeleteModel):
    """Evento que combina timestamps y soft delete"""

    EVENT_TYPES = [
        ('INFO', 'Informativo'),
        ('WARNING', 'Advertencia'),
        ('ERROR', 'Error'),
    ]

    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    message = models.TextField()

    # Hereda:
    # - BaseModel: created_at, updated_at, is_active
    # - TimestampedModel: timestamp, device_timestamp
    # - SoftDeleteModel: deleted_at, deleted_by
```

### Uso en vistas

```python
def recent_events(request):
    """Vista que usa funcionalidades heredadas"""
    events = Event.objects.filter(is_active=True)

    # Usar propiedades heredadas
    recent = [e for e in events if e.is_recent]
    old_events = [e for e in events if e.age_days > 30]

    return JsonResponse({
        'recent_count': len(recent),
        'old_count': len(old_events)
    })
```

## 🚀 Próximos Pasos

1. **Ejecutar script de análisis** para identificar modelos candidatos
2. **Migrar modelos uno por uno** siguiendo el proceso
3. **Crear migraciones** y aplicarlas
4. **Actualizar serializers** si es necesario
5. **Probar funcionalidades** heredadas
6. **Documentar cambios** en cada app

## 📚 Referencias

- [Django Abstract Base Classes](https://docs.djangoproject.com/en/stable/topics/db/models/#abstract-base-classes)
- [Django Model Inheritance](https://docs.djangoproject.com/en/stable/topics/db/models/#model-inheritance)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/misc/api-stability/)
