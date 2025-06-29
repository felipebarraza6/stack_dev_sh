# SmartHydro Alert System

## Descripción

El **Alert System** es un microservicio FastAPI que monitorea variables en tiempo real y ejecuta alertas basadas en condiciones personalizables. Se integra con el sistema de notificaciones para enviar alertas automáticas cuando se cumplen ciertas condiciones.

## Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Variables     │    │   Alert         │    │  Notification   │
│   (Sensores,    │───►│   Service       │───►│  Service        │
│    APIs, etc.)  │    │   (FastAPI)     │    │  (FastAPI)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │     Redis       │
                       │   (Cache &      │
                       │   Cooldown)     │
                       └─────────────────┘
```

## Características

- **Monitoreo en tiempo real**: Variables de múltiples fuentes
- **Condiciones flexibles**: Operadores matemáticos, lógicos y funciones
- **Frecuencias personalizables**: Desde inmediato hasta semanal
- **Cooldown inteligente**: Evita spam de alertas
- **Acciones múltiples**: Notificaciones, webhooks, emails
- **Scheduler automático**: Ejecución periódica de reglas
- **Métricas y estadísticas**: Monitoreo del sistema

## Tipos de Variables

### Variables de Telemetría

- `water_level`: Nivel de agua
- `flow_rate`: Caudal
- `temperature`: Temperatura
- `pressure`: Presión
- `ph_level`: Nivel de pH
- `turbidity`: Turbidez

### Variables Financieras

- `account_balance`: Saldo de cuenta
- `payment_amount`: Monto de pago
- `transaction_count`: Número de transacciones
- `daily_revenue`: Ingresos diarios

### Variables del Sistema

- `cpu_usage`: Uso de CPU
- `memory_usage`: Uso de memoria
- `disk_space`: Espacio en disco
- `active_connections`: Conexiones activas

## Operadores de Condición

### Comparación

- `eq`: Igual a (=)
- `ne`: Diferente a (≠)
- `gt`: Mayor que (>)
- `gte`: Mayor o igual que (≥)
- `lt`: Menor que (<)
- `lte`: Menor o igual que (≤)

### Texto

- `contains`: Contiene
- `not_contains`: No contiene

### Listas

- `in`: Está en lista
- `not_in`: No está en lista

### Especiales

- `between`: Entre valores
- `is_null`: Es nulo
- `is_not_null`: No es nulo

## Funciones de Agregación

### Estadísticas

- `avg`: Promedio
- `sum`: Suma
- `min`: Mínimo
- `max`: Máximo
- `count`: Conteo
- `std`: Desviación estándar

### Análisis

- `trend`: Tendencia (creciente/decreciente/estable)
- `change`: Cambio porcentual

## Frecuencias de Ejecución

- `immediate`: Inmediato (por eventos)
- `minute_1`: Cada minuto
- `minute_5`: Cada 5 minutos
- `minute_15`: Cada 15 minutos
- `minute_30`: Cada 30 minutos
- `hour_1`: Cada hora
- `hour_6`: Cada 6 horas
- `hour_12`: Cada 12 horas
- `day_1`: Diario
- `week_1`: Semanal

## Endpoints

### Gestión de Reglas

#### Crear Regla de Alerta

```http
POST /alerts/rules
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Alto Nivel de Agua",
  "description": "Alerta cuando el nivel de agua supera 80%",
  "module": "telemetry",
  "alert_type": "warning",
  "conditions": [
    {
      "variable_name": "water_level",
      "operator": "gt",
      "value": 80,
      "function": "avg",
      "time_window": 5
    }
  ],
  "actions": [
    {
      "action_type": "notification",
      "target": "operators",
      "template_name": "high_water_level",
      "parameters": {
        "user_ids": [1, 2, 3]
      }
    }
  ],
  "frequency": "minute_5",
  "priority": 8,
  "cooldown_minutes": 30
}
```

#### Obtener Reglas

```http
GET /alerts/rules?module=telemetry&is_active=true
Authorization: Bearer <token>
```

#### Actualizar Regla

```http
PUT /alerts/rules/{rule_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Alto Nivel de Agua - Actualizado",
  "conditions": [
    {
      "variable_name": "water_level",
      "operator": "gt",
      "value": 85
    }
  ],
  "actions": [...],
  "frequency": "minute_1"
}
```

#### Activar/Desactivar Regla

```http
POST /alerts/rules/{rule_id}/activate
POST /alerts/rules/{rule_id}/deactivate
Authorization: Bearer <token>
```

### Ejecución de Alertas

#### Ejecutar Regla Manualmente

```http
POST /alerts/execute
Authorization: Bearer <token>
Content-Type: application/json

{
  "rule_id": 123
}
```

#### Ejecutar Todas las Reglas

```http
POST /alerts/execute-all
Authorization: Bearer <token>
```

#### Historial de Ejecuciones

```http
GET /alerts/executions?rule_id=123&status=triggered&limit=20
Authorization: Bearer <token>
```

### Variables

#### Enviar Datos de Variable

```http
POST /variables/data
Authorization: Bearer <token>
Content-Type: application/json

{
  "variable_name": "water_level",
  "value": 75.5,
  "timestamp": "2024-01-15T10:30:00-03:00",
  "source": "sensor_001",
  "metadata": {
    "location": "reservoir_1",
    "unit": "cm"
  }
}
```

#### Variables Disponibles

```http
GET /variables/available
Authorization: Bearer <token>
```

#### Historial de Variable

```http
GET /variables/{variable_name}/history?hours=24
Authorization: Bearer <token>
```

### Utilidades

#### Operadores Disponibles

```http
GET /conditions/operators
```

#### Funciones Disponibles

```http
GET /conditions/functions
```

#### Módulos Disponibles

```http
GET /modules
```

#### Tipos de Alerta

```http
GET /alert-types
```

### Métricas

#### Métricas del Servicio

```http
GET /metrics
Authorization: Bearer <token>
```

#### Estadísticas de Alertas

```http
GET /alerts/stats?days=7
Authorization: Bearer <token>
```

## Ejemplos de Reglas

### 1. Alerta de Nivel de Agua Alto

```json
{
  "name": "Nivel de Agua Crítico",
  "description": "Alerta cuando el nivel de agua supera 90%",
  "module": "telemetry",
  "alert_type": "critical",
  "conditions": [
    {
      "variable_name": "water_level",
      "operator": "gt",
      "value": 90,
      "function": "avg",
      "time_window": 10
    }
  ],
  "actions": [
    {
      "action_type": "notification",
      "target": "emergency_team",
      "template_name": "critical_water_level",
      "parameters": {
        "user_ids": [1, 2, 3, 4, 5]
      }
    },
    {
      "action_type": "webhook",
      "target": "https://api.emergency-system.com/alert",
      "parameters": {
        "priority": "critical",
        "category": "water_level"
      }
    }
  ],
  "frequency": "immediate",
  "priority": 10,
  "cooldown_minutes": 60
}
```

### 2. Alerta de Tendencia de Caudal

```json
{
  "name": "Caudal Decreciente",
  "description": "Alerta cuando el caudal muestra tendencia decreciente",
  "module": "telemetry",
  "alert_type": "warning",
  "conditions": [
    {
      "variable_name": "flow_rate",
      "operator": "eq",
      "value": "decreasing",
      "function": "trend",
      "time_window": 30
    }
  ],
  "actions": [
    {
      "action_type": "notification",
      "target": "operators",
      "template_name": "flow_rate_decreasing",
      "parameters": {
        "user_ids": [1, 2]
      }
    }
  ],
  "frequency": "minute_15",
  "priority": 6,
  "cooldown_minutes": 120
}
```

### 3. Alerta de Saldo Bajo

```json
{
  "name": "Saldo Bancario Bajo",
  "description": "Alerta cuando el saldo está por debajo de $10,000",
  "module": "banking",
  "alert_type": "warning",
  "conditions": [
    {
      "variable_name": "account_balance",
      "operator": "lt",
      "value": 10000
    }
  ],
  "actions": [
    {
      "action_type": "notification",
      "target": "finance_team",
      "template_name": "low_balance",
      "parameters": {
        "user_ids": [10, 11, 12]
      }
    },
    {
      "action_type": "email",
      "target": "finance@smarthydro.com",
      "template_name": "low_balance_email"
    }
  ],
  "frequency": "hour_1",
  "priority": 7,
  "cooldown_minutes": 240
}
```

### 4. Alerta de Cambio Rápido de pH

```json
{
  "name": "Cambio Rápido de pH",
  "description": "Alerta cuando el pH cambia más del 20% en 5 minutos",
  "module": "telemetry",
  "alert_type": "error",
  "conditions": [
    {
      "variable_name": "ph_level",
      "operator": "gt",
      "value": 20,
      "function": "change",
      "time_window": 5
    }
  ],
  "actions": [
    {
      "action_type": "notification",
      "target": "quality_team",
      "template_name": "ph_change_alert",
      "parameters": {
        "user_ids": [20, 21, 22]
      }
    }
  ],
  "frequency": "immediate",
  "priority": 9,
  "cooldown_minutes": 30
}
```

## Integración con Otros Servicios

### Enviar Datos desde Telemetría

```python
# En telemetry-collector
import httpx
import asyncio

async def send_alert_data(variable_name: str, value: float, source: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://alert-service:8007/variables/data",
            json={
                "variable_name": variable_name,
                "value": value,
                "source": source,
                "timestamp": datetime.now().isoformat()
            }
        )

# Ejemplo de uso
await send_alert_data("water_level", 85.5, "sensor_reservoir_1")
```

### Enviar Datos desde Django

```python
# En cualquier módulo de Django
import httpx
import asyncio

async def send_banking_alert_data(account_id: int, balance: float):
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://alert-service:8007/variables/data",
            json={
                "variable_name": f"account_balance_{account_id}",
                "value": balance,
                "source": "banking_system",
                "metadata": {
                    "account_id": account_id,
                    "currency": "CLP"
                }
            }
        )

# En signal de Django
@receiver(post_save, sender=Account)
def notify_balance_change(sender, instance, **kwargs):
    asyncio.create_task(
        send_banking_alert_data(instance.id, instance.balance)
    )
```

## Configuración

### Variables de Entorno

```bash
# Base de datos
DATABASE_URL=postgresql://smarthydro:smarthydro123@postgres:5432/smarthydro_business

# Redis para cache y cooldown
REDIS_URL=redis://:smarthydro123@redis:6379

# Servicios externos
DJANGO_API_URL=http://business-api:8004
NOTIFICATION_SERVICE_URL=http://notification-service:8006
TELEMETRY_SERVICE_URL=http://telemetry-collector:8001

# Configuración general
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### Docker Compose

```yaml
alert-service:
  build:
    context: ./services/alert-service
    dockerfile: Dockerfile
  container_name: smarthydro-alert-service
  environment:
    - DATABASE_URL=postgresql://smarthydro:${POSTGRES_PASSWORD:-smarthydro123}@postgres:5432/smarthydro_business
    - REDIS_URL=redis://:${REDIS_PASSWORD:-smarthydro123}@redis:6379
    - DJANGO_API_URL=http://business-api:8004
    - NOTIFICATION_SERVICE_URL=http://notification-service:8006
    - TELEMETRY_SERVICE_URL=http://telemetry-collector:8001
    - LOG_LEVEL=INFO
    - ENVIRONMENT=development
  ports:
    - "8007:8007"
  depends_on:
    - redis
    - business-api
    - notification-service
  networks:
    - smarthydro-network
```

## Base de Datos

### Tablas Requeridas

```sql
-- Reglas de alerta
CREATE TABLE alerts_rule (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    module VARCHAR(50) NOT NULL,
    alert_type VARCHAR(20) NOT NULL,
    conditions JSONB NOT NULL,
    actions JSONB NOT NULL,
    frequency VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    is_active BOOLEAN DEFAULT true,
    priority INTEGER DEFAULT 1,
    cooldown_minutes INTEGER DEFAULT 0,
    last_execution TIMESTAMP,
    next_execution TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by INTEGER
);

-- Ejecuciones de alerta
CREATE TABLE alerts_execution (
    id SERIAL PRIMARY KEY,
    rule_id INTEGER REFERENCES alerts_rule(id),
    status VARCHAR(20) NOT NULL,
    triggered BOOLEAN DEFAULT false,
    execution_time TIMESTAMP NOT NULL,
    duration_ms INTEGER,
    error_message TEXT,
    condition_results JSONB,
    action_results JSONB,
    variable_values JSONB
);

-- Datos de variables
CREATE TABLE alerts_variable_data (
    id SERIAL PRIMARY KEY,
    variable_name VARCHAR(255) NOT NULL,
    value JSONB NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    source VARCHAR(100),
    metadata JSONB,
    INDEX idx_variable_timestamp (variable_name, timestamp)
);
```

## Monitoreo y Métricas

### Health Check

```bash
curl http://localhost:8007/health
```

### Métricas del Servicio

```bash
curl -H "Authorization: Bearer <token>" http://localhost:8007/metrics
```

### Estadísticas de Alertas

```bash
curl -H "Authorization: Bearer <token>" http://localhost:8007/alerts/stats?days=7
```

## Troubleshooting

### Problemas Comunes

#### Reglas No Se Ejecutan

```bash
# Verificar reglas activas
curl -H "Authorization: Bearer <token>" http://localhost:8007/alerts/rules?is_active=true

# Verificar scheduler
docker logs smarthydro-alert-service | grep scheduler
```

#### Variables No Llegan

```bash
# Verificar variables disponibles
curl -H "Authorization: Bearer <token>" http://localhost:8007/variables/available

# Verificar conectividad
docker exec smarthydro-alert-service ping telemetry-collector
```

#### Alertas No Se Disparan

```bash
# Verificar condiciones
curl -H "Authorization: Bearer <token>" http://localhost:8007/alerts/executions?status=not_triggered

# Verificar cooldown
docker exec smarthydro-redis redis-cli keys "alert_cooldown:*"
```

## Desarrollo

### Estructura del Proyecto

```
services/alert-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app principal
│   ├── models.py            # Modelos Pydantic
│   ├── alert_manager.py     # Lógica de alertas
│   └── auth.py              # Autenticación
├── Dockerfile
└── requirements.txt
```

### Testing

```bash
# Ejecutar tests
cd services/alert-service
python -m pytest

# Test de integración
curl -X POST http://localhost:8007/variables/data \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"variable_name": "test_var", "value": 100}'
```

## Flujo Completo de Ejemplo

### 1. Crear Regla de Alerta

```bash
curl -X POST http://localhost:8007/alerts/rules \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Alert",
    "module": "telemetry",
    "alert_type": "warning",
    "conditions": [{
      "variable_name": "test_var",
      "operator": "gt",
      "value": 50
    }],
    "actions": [{
      "action_type": "notification",
      "target": "test",
      "template_name": "test_alert"
    }],
    "frequency": "immediate"
  }'
```

### 2. Enviar Datos de Variable

```bash
curl -X POST http://localhost:8007/variables/data \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "variable_name": "test_var",
    "value": 75,
    "source": "test"
  }'
```

### 3. Verificar Ejecución

```bash
curl -H "Authorization: Bearer <token>" http://localhost:8007/alerts/executions
```

### 4. Verificar Notificación

```bash
curl -H "Authorization: Bearer <token>" http://localhost:8006/notifications/user/1
```

¡El sistema de alertas está **100% funcional** y **integrado** con tu arquitectura de microservicios! 🚀
