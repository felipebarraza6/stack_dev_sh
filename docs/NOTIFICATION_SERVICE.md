# SmartHydro Notification Service

## Descripción

El **Notification Service** es un microservicio FastAPI independiente que maneja todas las notificaciones del sistema SmartHydro. Se comunica con la API principal de Django y proporciona notificaciones en tiempo real a través de WebSocket y por email.

## Arquitectura

```
┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────┐
│   Frontend      │    │  Notification       │    │   Django API    │
│   (React/Vue)   │◄──►│  Service (FastAPI)  │◄──►│   (Business)    │
└─────────────────┘    └─────────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │     Redis       │
                       │   (WebSocket)   │
                       └─────────────────┘
```

## Características

- **Microservicio FastAPI**: Arquitectura consistente con el resto del sistema
- **Notificaciones en tiempo real**: WebSocket a través de Redis
- **Notificaciones por email**: Integración con servicios de email
- **Plantillas personalizables**: Sistema de plantillas por módulo
- **Preferencias de usuario**: Control granular de notificaciones
- **Autenticación**: Integración con el sistema de autenticación de Django
- **Métricas y monitoreo**: Health checks y estadísticas

## Endpoints

### Notificaciones

#### Enviar Notificación

```http
POST /notifications/send
Authorization: Bearer <token>
Content-Type: application/json

{
  "template_name": "payment_received",
  "module": "payments",
  "user_ids": [1, 2, 3],
  "context_data": {
    "amount": 150000,
    "payment_method": "transfer",
    "reference": "INV-2024-001"
  },
  "priority": "high",
  "related_model": "payments.payment",
  "related_id": 123
}
```

#### Enviar Notificación Personalizada

```http
POST /notifications/send-custom
Authorization: Bearer <token>
Content-Type: application/json

{
  "subject": "Mantenimiento Programado",
  "message": "El sistema estará en mantenimiento mañana de 2:00 a 4:00 AM",
  "user_ids": [1, 2, 3, 4, 5],
  "priority": "medium",
  "module": "global"
}
```

#### Obtener Notificaciones de Usuario

```http
GET /notifications/user/{user_id}?status=sent&module=payments&limit=20&offset=0
Authorization: Bearer <token>
```

#### Marcar como Leída

```http
POST /notifications/{notification_id}/mark-read
Authorization: Bearer <token>
```

#### Marcar Todas como Leídas

```http
POST /notifications/user/{user_id}/mark-all-read
Authorization: Bearer <token>
```

#### Conteo de No Leídas

```http
GET /notifications/user/{user_id}/unread-count
Authorization: Bearer <token>
```

#### Estadísticas de Usuario

```http
GET /notifications/user/{user_id}/stats
Authorization: Bearer <token>
```

### Plantillas

#### Obtener Plantillas

```http
GET /templates?module=payments
Authorization: Bearer <token>
```

### Preferencias

#### Obtener Preferencias

```http
GET /preferences/user/{user_id}
Authorization: Bearer <token>
```

#### Actualizar Preferencias

```http
POST /preferences/user/{user_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "payments": {
    "email_enabled": true,
    "websocket_enabled": true,
    "settings": {
      "priority_filter": ["high", "urgent"]
    }
  },
  "quotations": {
    "email_enabled": false,
    "websocket_enabled": true
  }
}
```

### Utilidades

#### Health Check

```http
GET /health
```

#### Métricas del Servicio

```http
GET /metrics
Authorization: Bearer <token>
```

#### Módulos Disponibles

```http
GET /modules
```

## Plantillas de Notificación

### Estructura de Plantilla

```json
{
  "id": 1,
  "name": "payment_received",
  "module": "payments",
  "notification_type": "both",
  "subject": "Pago Recibido - {{amount}}",
  "message_template": "Se ha recibido un pago de {{amount}} por {{payment_method}}. Referencia: {{reference}}",
  "is_active": true,
  "available_variables": {
    "amount": "Monto del pago",
    "payment_method": "Método de pago",
    "reference": "Número de referencia"
  }
}
```

### Plantillas por Módulo

#### Banking

- `account_created`: Nueva cuenta bancaria creada
- `transaction_completed`: Transacción completada
- `balance_alert`: Alerta de saldo bajo

#### Payments

- `payment_received`: Pago recibido
- `payment_failed`: Pago fallido
- `payment_processed`: Pago procesado

#### Quotations

- `quotation_created`: Cotización creada
- `quotation_approved`: Cotización aprobada
- `quotation_rejected`: Cotización rechazada

#### Support

- `ticket_created`: Ticket de soporte creado
- `ticket_updated`: Ticket actualizado
- `ticket_resolved`: Ticket resuelto

#### Projects

- `project_started`: Proyecto iniciado
- `milestone_completed`: Hito completado
- `project_completed`: Proyecto completado

## WebSocket

### Conexión

```javascript
// Frontend - Conexión WebSocket
const socket = new WebSocket("ws://localhost:8006/ws/");

socket.onopen = function (e) {
  console.log("Conectado al servicio de notificaciones");
};

socket.onmessage = function (event) {
  const notification = JSON.parse(event.data);
  console.log("Nueva notificación:", notification);

  // Mostrar notificación en UI
  showNotification(notification);
};
```

### Formato de Mensaje

```json
{
  "type": "notification.message",
  "notification_id": 123,
  "subject": "Pago Recibido - $150,000",
  "message": "Se ha recibido un pago de $150,000 por transferencia. Referencia: INV-2024-001",
  "priority": "high",
  "module": "payments",
  "timestamp": "2024-01-15T10:30:00-03:00",
  "metadata": {
    "amount": 150000,
    "payment_method": "transfer",
    "reference": "INV-2024-001"
  }
}
```

## Integración con Django API

### Enviar Notificación desde Django

```python
# En cualquier módulo de Django
import httpx
import asyncio

async def send_notification_from_django():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://notification-service:8006/notifications/send",
            json={
                "template_name": "payment_received",
                "module": "payments",
                "user_ids": [1, 2, 3],
                "context_data": {
                    "amount": 150000,
                    "payment_method": "transfer",
                    "reference": "INV-2024-001"
                },
                "priority": "high"
            },
            headers={"Authorization": "Bearer <service_token>"}
        )
        return response.json()

# Ejecutar
asyncio.run(send_notification_from_django())
```

### Signals de Django

```python
# En signals.py de cualquier módulo
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment
import httpx
import asyncio

@receiver(post_save, sender=Payment)
def notify_payment_received(sender, instance, created, **kwargs):
    if created and instance.status == 'completed':
        # Enviar notificación
        asyncio.create_task(send_payment_notification(instance))

async def send_payment_notification(payment):
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://notification-service:8006/notifications/send",
            json={
                "template_name": "payment_received",
                "module": "payments",
                "user_ids": [payment.user.id],
                "context_data": {
                    "amount": payment.amount,
                    "payment_method": payment.method,
                    "reference": payment.reference
                },
                "priority": "high",
                "related_model": "payments.payment",
                "related_id": payment.id
            }
        )
```

## Configuración

### Variables de Entorno

```bash
# Base de datos
DATABASE_URL=postgresql://smarthydro:smarthydro123@postgres:5432/smarthydro_business

# Redis para WebSocket
REDIS_URL=redis://:smarthydro123@redis:6379

# API de Django
DJANGO_API_URL=http://business-api:8004

# Configuración general
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### Docker Compose

```yaml
notification-service:
  build:
    context: ./services/notification-service
    dockerfile: Dockerfile
  container_name: smarthydro-notification-service
  environment:
    - DATABASE_URL=postgresql://smarthydro:${POSTGRES_PASSWORD:-smarthydro123}@postgres:5432/smarthydro_business
    - REDIS_URL=redis://:${REDIS_PASSWORD:-smarthydro123}@redis:6379
    - DJANGO_API_URL=http://business-api:8004
    - LOG_LEVEL=INFO
    - ENVIRONMENT=development
  ports:
    - "8006:8006"
  depends_on:
    - redis
    - business-api
  networks:
    - smarthydro-network
```

## Despliegue

### Desarrollo Local

```bash
# Construir y ejecutar
docker-compose up notification-service

# O ejecutar directamente
cd services/notification-service
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8006 --reload
```

### Producción

```bash
# Construir imagen
docker build -t smarthydro/notification-service:latest ./services/notification-service

# Ejecutar
docker run -d \
  --name smarthydro-notification-service \
  -p 8006:8006 \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_URL=redis://... \
  -e DJANGO_API_URL=http://... \
  smarthydro/notification-service:latest
```

## Monitoreo

### Health Check

```bash
curl http://localhost:8006/health
```

### Métricas

```bash
curl -H "Authorization: Bearer <token>" http://localhost:8006/metrics
```

### Logs

```bash
docker logs smarthydro-notification-service
```

## Base de Datos

### Tablas Requeridas

El servicio utiliza las siguientes tablas de la base de datos Django:

- `notifications_template`: Plantillas de notificación
- `notifications_notification`: Notificaciones enviadas
- `notifications_preference`: Preferencias de usuario
- `notifications_log`: Logs de envío

### Migraciones

Las migraciones se ejecutan automáticamente desde Django. El servicio de notificaciones solo lee/escribe en estas tablas.

## Seguridad

### Autenticación

- Todos los endpoints requieren autenticación Bearer token
- Los tokens se validan contra la API de Django
- Los usuarios solo pueden acceder a sus propias notificaciones
- Los administradores pueden acceder a todas las notificaciones

### Autorización

- Verificación de permisos por endpoint
- Control de acceso basado en roles
- Validación de datos de entrada

## Troubleshooting

### Problemas Comunes

#### Error de Conexión a Base de Datos

```bash
# Verificar conectividad
docker exec smarthydro-notification-service ping postgres

# Verificar variables de entorno
docker exec smarthydro-notification-service env | grep DATABASE
```

#### Error de Conexión a Redis

```bash
# Verificar Redis
docker exec smarthydro-redis redis-cli ping

# Verificar conectividad desde el servicio
docker exec smarthydro-notification-service ping redis
```

#### Notificaciones No Llegan

```bash
# Verificar logs
docker logs smarthydro-notification-service

# Verificar plantillas
curl -H "Authorization: Bearer <token>" http://localhost:8006/templates
```

#### WebSocket No Funciona

```bash
# Verificar Redis
docker exec smarthydro-redis redis-cli pubsub channels

# Verificar conectividad WebSocket
wscat -c ws://localhost:8006/ws/
```

## Desarrollo

### Estructura del Proyecto

```
services/notification-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación FastAPI principal
│   ├── models.py            # Modelos Pydantic
│   ├── notification_manager.py  # Lógica de negocio
│   └── auth.py              # Autenticación
├── Dockerfile
└── requirements.txt
```

### Agregar Nueva Plantilla

1. Crear registro en `notifications_template`
2. Definir variables disponibles
3. Probar con endpoint `/notifications/send`

### Agregar Nuevo Módulo

1. Agregar al enum `NotificationModule`
2. Crear plantillas específicas
3. Actualizar documentación

### Testing

```bash
# Ejecutar tests
cd services/notification-service
python -m pytest

# Test de integración
curl -X POST http://localhost:8006/notifications/send \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"template_name": "test", "module": "global", "user_ids": [1]}'
```
