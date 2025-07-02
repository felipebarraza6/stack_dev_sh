# Configuración Modular de Django REST Framework

## Estructura de Configuración DRF

La configuración de Django REST Framework ahora está organizada de manera modular para facilitar el manejo de diferentes entornos (desarrollo y producción).

### Estructura de Archivos

```
api/config/drf/
├── __init__.py          # Exporta la configuración base
├── base.py              # Configuración común para todos los entornos
├── development.py       # Configuración específica para desarrollo
└── production.py        # Configuración específica para producción
```

### Configuración Base (`base.py`)

Contiene la configuración común que se aplica a todos los entornos:

- **Paginación dinámica**: Permite definir `page_size` en la consulta (máximo 100 elementos)
- **Autenticación personalizada**: Token authentication con mejor manejo de errores
- **Throttling**: Rate limiting para usuarios autenticados y anónimos
- **Filtros y búsqueda**: Django filters, búsqueda y ordenamiento
- **Formatos de fecha**: Configuración estándar para fechas y horas

### Configuración de Desarrollo (`development.py`)

Configuración más permisiva para facilitar el desarrollo:

- **Renderer adicional**: Incluye `BrowsableAPIRenderer` para interfaz web
- **Throttling deshabilitado**: Para facilitar testing
- **Paginación más permisiva**: 20 elementos por defecto
- **Caché más corta**: 1 minuto
- **Logging detallado**: Nivel DEBUG para DRF

### Configuración de Producción (`production.py`)

Configuración más estricta y segura para producción:

- **Solo JSON**: Solo renderer JSON (más seguro)
- **Throttling estricto**: Límites más bajos para protección
- **Paginación conservadora**: 10 elementos por defecto
- **Caché más larga**: 10 minutos
- **Seguridad adicional**: Configuraciones de seguridad específicas

## Uso Automático

La configuración se aplica automáticamente según el entorno:

### Desarrollo

```python
# api/config/settings/development.py
from api.config.drf.development import REST_FRAMEWORK_DEV
REST_FRAMEWORK = REST_FRAMEWORK_DEV
```

### Producción

```python
# api/config/settings/production.py
from api.config.drf.production import REST_FRAMEWORK_PROD
REST_FRAMEWORK = REST_FRAMEWORK_PROD
```

## Características Principales

### 1. Paginación Dinámica

```python
# Ejemplo de uso
GET /api/telemetry/?page=2&page_size=25
```

**Respuesta:**

```json
{
    "count": 150,
    "next": "http://api.example.com/telemetry/?page=3&page_size=25",
    "previous": "http://api.example.com/telemetry/?page=1&page_size=25",
    "results": [...],
    "page_info": {
        "current_page": 2,
        "total_pages": 6,
        "page_size": 25,
        "has_next": true,
        "has_previous": true
    }
}
```

### 2. Throttling Inteligente

- **Desarrollo**: Throttling deshabilitado
- **Producción**:
  - Usuarios autenticados: 500 requests/hora
  - Usuarios anónimos: 50 requests/hora
  - Burst protection: 30 requests/minuto

### 3. Autenticación Mejorada

```python
# Headers requeridos
Authorization: Token your-token-here
```

### 4. Filtros y Búsqueda

```python
# Ejemplos de uso
GET /api/telemetry/?search=temperatura
GET /api/telemetry/?ordering=-timestamp
GET /api/telemetry/?device_id=123
```

## Configuración de Entorno

### Variables de Entorno

```bash
# Para desarrollo
export DJANGO_SETTINGS_MODULE=api.config.settings.development

# Para producción
export DJANGO_SETTINGS_MODULE=api.config.settings.production
```

### Docker

```yaml
# docker-compose.yml
environment:
  - DJANGO_SETTINGS_MODULE=api.config.settings.development
```

## Beneficios de la Configuración Modular

1. **Separación de Responsabilidades**: Cada entorno tiene su configuración específica
2. **Mantenimiento Fácil**: Cambios centralizados en archivos específicos
3. **Seguridad**: Configuraciones más estrictas en producción
4. **Desarrollo Eficiente**: Configuraciones permisivas en desarrollo
5. **Escalabilidad**: Fácil agregar nuevos entornos (staging, testing, etc.)

## Extensibilidad

Para agregar un nuevo entorno (ej: staging):

1. Crear `api/config/drf/staging.py`
2. Importar desde `base.py`
3. Personalizar según necesidades
4. Actualizar `api/config/settings/staging.py`

```python
# api/config/drf/staging.py
from .base import REST_FRAMEWORK

REST_FRAMEWORK_STAGING = REST_FRAMEWORK.copy()
# Personalizar configuración para staging
```

## Logging y Monitoreo

### Desarrollo

- Logs detallados en consola y archivo
- Nivel DEBUG para DRF
- SQL logging habilitado

### Producción

- Logs de nivel WARNING y ERROR
- Formato verbose con timestamp
- Logs separados por aplicación

## Consideraciones de Seguridad

### Producción

- Solo renderer JSON
- Throttling estricto
- Autenticación por token únicamente
- Headers de seguridad habilitados
- CORS restrictivo

### Desarrollo

- Renderer web habilitado
- Throttling deshabilitado
- CORS permisivo
- Logging detallado
