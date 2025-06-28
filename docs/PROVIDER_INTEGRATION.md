# Integración de Proveedores de Telemetría

## 🎯 **Visión General**

El sistema SmartHydro está diseñado para integrar múltiples proveedores de telemetría de manera modular y escalable. Agregar un nuevo proveedor es tan simple como crear un endpoint y configurar la consulta de datos.

## 🏗️ **Arquitectura de Proveedores**

### **Estructura Modular**

```
telemetry-collector/
├── app/
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── base.py              # Clase base para proveedores
│   │   ├── twin.py              # Twin Data
│   │   ├── nettra.py            # Nettra
│   │   ├── novus.py             # Novus
│   │   └── custom_provider.py   # Nuevo proveedor
│   ├── config/
│   │   └── providers.yaml       # Configuración de proveedores
│   └── api/
│       └── providers.py         # Endpoints de proveedores
```

## 🔧 **Clase Base para Proveedores**

### **BaseProvider Class**

```python
# app/providers/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import asyncio
import aiohttp
from datetime import datetime

class BaseProvider(ABC):
    """Clase base para todos los proveedores de telemetría"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get('name', 'unknown')
        self.base_url = config.get('base_url')
        self.api_key = config.get('api_key')
        self.timeout = config.get('timeout', 30)

    @abstractmethod
    async def authenticate(self) -> bool:
        """Autenticación con el proveedor"""
        pass

    @abstractmethod
    async def get_data(self, point_config: Dict[str, Any]) -> Dict[str, Any]:
        """Obtener datos del punto de captación"""
        pass

    @abstractmethod
    async def validate_response(self, response: Dict[str, Any]) -> bool:
        """Validar respuesta del proveedor"""
        pass

    async def health_check(self) -> Dict[str, Any]:
        """Health check del proveedor"""
        try:
            is_authenticated = await self.authenticate()
            return {
                'provider': self.name,
                'status': 'healthy' if is_authenticated else 'unhealthy',
                'timestamp': datetime.utcnow().isoformat(),
                'response_time': 0  # Implementar medición
            }
        except Exception as e:
            return {
                'provider': self.name,
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }

    def transform_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transformar datos al formato estándar"""
        return {
            'value': raw_data.get('value', 0),
            'unit': raw_data.get('unit', ''),
            'timestamp': raw_data.get('timestamp'),
            'quality': raw_data.get('quality', 1.0),
            'metadata': {
                'provider': self.name,
                'raw_data': raw_data
            }
        }
```

## 📋 **Implementación de Proveedores**

### **1. Twin Data Provider**

```python
# app/providers/twin.py
import aiohttp
from .base import BaseProvider

class TwinDataProvider(BaseProvider):
    """Proveedor Twin Data"""

    async def authenticate(self) -> bool:
        """Autenticación con Twin Data"""
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/auth/verify",
                    headers=headers,
                    timeout=self.timeout
                ) as response:
                    return response.status == 200
        except Exception:
            return False

    async def get_data(self, point_config: Dict[str, Any]) -> Dict[str, Any]:
        """Obtener datos de Twin Data"""
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            variable = point_config.get('variable')

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/data/{variable}",
                    headers=headers,
                    timeout=self.timeout
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self.transform_data(data)
                    else:
                        raise Exception(f"Error {response.status}: {await response.text()}")
        except Exception as e:
            raise Exception(f"Error getting data from Twin Data: {str(e)}")

    async def validate_response(self, response: Dict[str, Any]) -> bool:
        """Validar respuesta de Twin Data"""
        required_fields = ['value', 'timestamp']
        return all(field in response for field in required_fields)
```

### **2. Nettra Provider**

```python
# app/providers/nettra.py
import aiohttp
from .base import BaseProvider

class NettraProvider(BaseProvider):
    """Proveedor Nettra (The Things Network)"""

    async def authenticate(self) -> bool:
        """Autenticación con Nettra"""
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/applications",
                    headers=headers,
                    timeout=self.timeout
                ) as response:
                    return response.status == 200
        except Exception:
            return False

    async def get_data(self, point_config: Dict[str, Any]) -> Dict[str, Any]:
        """Obtener datos de Nettra"""
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            device_id = point_config.get('device_id')

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/devices/{device_id}/packages",
                    headers=headers,
                    timeout=self.timeout
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self.transform_data(data)
                    else:
                        raise Exception(f"Error {response.status}: {await response.text()}")
        except Exception as e:
            raise Exception(f"Error getting data from Nettra: {str(e)}")

    async def validate_response(self, response: Dict[str, Any]) -> bool:
        """Validar respuesta de Nettra"""
        required_fields = ['result', 'timestamp']
        return all(field in response for field in required_fields)
```

### **3. Novus Provider**

```python
# app/providers/novus.py
import aiohttp
from .base import BaseProvider

class NovusProvider(BaseProvider):
    """Proveedor Novus (Tago.io)"""

    async def authenticate(self) -> bool:
        """Autenticación con Novus"""
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/account/profile",
                    headers=headers,
                    timeout=self.timeout
                ) as response:
                    return response.status == 200
        except Exception:
            return False

    async def get_data(self, point_config: Dict[str, Any]) -> Dict[str, Any]:
        """Obtener datos de Novus"""
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            device_id = point_config.get('device_id')
            variable = point_config.get('variable')

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/data/{device_id}/{variable}",
                    headers=headers,
                    timeout=self.timeout
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self.transform_data(data)
                    else:
                        raise Exception(f"Error {response.status}: {await response.text()}")
        except Exception as e:
            raise Exception(f"Error getting data from Novus: {str(e)}")

    async def validate_response(self, response: Dict[str, Any]) -> bool:
        """Validar respuesta de Novus"""
        required_fields = ['value', 'time']
        return all(field in response for field in required_fields)
```

## 🔧 **Configuración de Proveedores**

### **Archivo de Configuración**

```yaml
# config/providers.yaml
providers:
  twin:
    name: "Twin Data"
    base_url: "https://api.twindata.com/v1"
    timeout: 30
    retry_attempts: 3
    retry_delay: 5

  nettra:
    name: "Nettra"
    base_url: "https://eu1.cloud.thethings.network/api/v3"
    timeout: 30
    retry_attempts: 3
    retry_delay: 5

  novus:
    name: "Novus"
    base_url: "https://api.tago.io"
    timeout: 30
    retry_attempts: 3
    retry_delay: 5

  custom_provider:
    name: "Custom Provider"
    base_url: "https://api.customprovider.com"
    timeout: 30
    retry_attempts: 3
    retry_delay: 5
```

### **Configuración de Puntos**

```yaml
# Ejemplo de configuración de punto
point_config:
  point_id: "point_123"
  provider: "twin"
  variable: "flow_sensor_01"
  frequency: "60"
  retry_on_failure: true
  max_retries: 3
  custom_headers:
    X-Custom-Header: "value"
  custom_params:
    format: "json"
    limit: 1
```

## 🚀 **Agregar Nuevo Proveedor**

### **Paso 1: Crear Clase del Proveedor**

```python
# app/providers/custom_provider.py
from .base import BaseProvider

class CustomProvider(BaseProvider):
    """Proveedor personalizado"""

    async def authenticate(self) -> bool:
        # Implementar autenticación
        pass

    async def get_data(self, point_config: Dict[str, Any]) -> Dict[str, Any]:
        # Implementar obtención de datos
        pass

    async def validate_response(self, response: Dict[str, Any]) -> bool:
        # Implementar validación
        pass
```

### **Paso 2: Registrar Proveedor**

```python
# app/providers/__init__.py
from .twin import TwinDataProvider
from .nettra import NettraProvider
from .novus import NovusProvider
from .custom_provider import CustomProvider

PROVIDERS = {
    'twin': TwinDataProvider,
    'nettra': NettraProvider,
    'novus': NovusProvider,
    'custom': CustomProvider
}

def get_provider(provider_name: str, config: Dict[str, Any]):
    """Obtener instancia del proveedor"""
    if provider_name not in PROVIDERS:
        raise ValueError(f"Provider {provider_name} not found")

    provider_class = PROVIDERS[provider_name]
    return provider_class(config)
```

### **Paso 3: Configurar en YAML**

```yaml
# config/providers.yaml
providers:
  custom:
    name: "Custom Provider"
    base_url: "https://api.customprovider.com"
    timeout: 30
    retry_attempts: 3
    retry_delay: 5
```

## 📊 **Endpoints de API**

### **Health Check de Proveedores**

```python
# app/api/providers.py
from fastapi import APIRouter, HTTPException
from app.providers import get_provider
from app.config import get_provider_config

router = APIRouter()

@router.get("/health/{provider_name}")
async def provider_health(provider_name: str):
    """Health check de un proveedor específico"""
    try:
        config = get_provider_config(provider_name)
        provider = get_provider(provider_name, config)
        health = await provider.health_check()
        return health
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def all_providers_health():
    """Health check de todos los proveedores"""
    providers = ['twin', 'nettra', 'novus']
    results = {}

    for provider_name in providers:
        try:
            config = get_provider_config(provider_name)
            provider = get_provider(provider_name, config)
            results[provider_name] = await provider.health_check()
        except Exception as e:
            results[provider_name] = {
                'status': 'error',
                'error': str(e)
            }

    return results
```

## 🔄 **Recolección de Datos**

### **Scheduler de Recolección**

```python
# app/scheduler/collector.py
import asyncio
from datetime import datetime
from app.providers import get_provider
from app.config import get_points_config

class DataCollector:
    """Recolector de datos de todos los proveedores"""

    async def collect_from_provider(self, provider_name: str, points: List[Dict]):
        """Recolectar datos de un proveedor específico"""
        try:
            config = get_provider_config(provider_name)
            provider = get_provider(provider_name, config)

            for point in points:
                if point['provider'] == provider_name:
                    try:
                        data = await provider.get_data(point['config'])
                        await self.publish_to_kafka(data)
                    except Exception as e:
                        await self.log_error(point['id'], str(e))
        except Exception as e:
            await self.log_error(provider_name, str(e))

    async def collect_all(self):
        """Recolectar datos de todos los proveedores"""
        points = get_points_config()

        # Agrupar puntos por proveedor
        providers_points = {}
        for point in points:
            provider = point['provider']
            if provider not in providers_points:
                providers_points[provider] = []
            providers_points[provider].append(point)

        # Recolectar datos de cada proveedor
        tasks = []
        for provider_name, points in providers_points.items():
            task = self.collect_from_provider(provider_name, points)
            tasks.append(task)

        await asyncio.gather(*tasks, return_exceptions=True)
```

## 📈 **Monitoreo y Métricas**

### **Métricas por Proveedor**

```python
# app/metrics/provider_metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Métricas de proveedores
provider_requests = Counter(
    'provider_requests_total',
    'Total requests to providers',
    ['provider', 'status']
)

provider_response_time = Histogram(
    'provider_response_time_seconds',
    'Provider response time',
    ['provider']
)

provider_health = Gauge(
    'provider_health_status',
    'Provider health status',
    ['provider']
)

def record_provider_metric(provider: str, status: str, duration: float):
    """Registrar métrica de proveedor"""
    provider_requests.labels(provider=provider, status=status).inc()
    provider_response_time.labels(provider=provider).observe(duration)
```

## 🎯 **Próximos Pasos**

1. **Implementar proveedores base**
2. **Configurar autenticación**
3. **Implementar validación de datos**
4. **Configurar métricas**
5. **Implementar retry logic**
6. **Configurar logging**
7. **Implementar tests**

## 📖 **Recursos de Aprendizaje**

### **Async Programming**

- [Python asyncio](https://docs.python.org/3/library/asyncio.html)
- [aiohttp](https://docs.aiohttp.org/)

### **API Design**

- [REST API Design](https://restfulapi.net/)
- [OpenAPI Specification](https://swagger.io/specification/)

### **Error Handling**

- [Python Exception Handling](https://docs.python.org/3/tutorial/errors.html)
- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)
