# Sistema de Notificaciones SmartHydro ERP

## 🎯 **Visión General**

El sistema de notificaciones de SmartHydro ERP es una solución completa y modular que permite enviar notificaciones en tiempo real a usuarios específicos cuando ocurren cambios importantes en cualquier módulo del sistema.

### **Características Principales**

- ✅ **Notificaciones en tiempo real** via WebSocket
- ✅ **Notificaciones por email** configurables
- ✅ **Sistema modular** por cada módulo del ERP
- ✅ **Plantillas personalizables** con variables dinámicas
- ✅ **Preferencias por usuario** y módulo
- ✅ **Logs completos** para auditoría
- ✅ **API REST** completa
- ✅ **Integración automática** con signals de Django

## 🏗️ **Arquitectura**

### **Componentes del Sistema**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Django Models │    │  Django Signals │    │  Notification   │
│   (ERP Modules) │───▶│   (Detect       │───▶│   Service       │
│                 │    │    Changes)     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   WebSocket     │◀───│  Redis Channel  │◀───│  Notification   │
│   Consumers     │    │   Layer         │    │   Templates     │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Flujo de Notificaciones**

1. **Evento ocurre** en un módulo del ERP (ej: transacción bancaria)
2. **Signal detecta** el cambio automáticamente
3. **NotificationService** procesa el evento
4. **Template** renderiza el mensaje con variables
5. **Envío** por email y/o WebSocket según preferencias
6. **Log** registra el resultado para auditoría

## 📋 **Módulos Soportados**

### **1. Banking (Bancario)**

- ✅ Transacciones procesadas
- ✅ Alertas de saldo bajo
- ✅ Transferencias entre cuentas

### **2. Payments (Pagos)**

- ✅ Pagos recibidos
- ✅ Pagos vencidos
- ✅ Programación de pagos

### **3. Quotations (Cotizaciones)**

- ✅ Cotizaciones aprobadas
- ✅ Cotizaciones rechazadas
- ✅ Cotizaciones por expirar

### **4. Invoicing (Facturación)**

- ✅ Facturas creadas
- ✅ Facturas vencidas
- ✅ Pagos de facturas

### **5. Support (Soporte)**

- ✅ Tickets asignados
- ✅ Cambios de estado en tickets
- ✅ Tickets de alta prioridad

### **6. Projects (Proyectos)**

- ✅ Proyectos creados
- ✅ Actualizaciones de proyectos

## 🔧 **Configuración**

### **1. Variables de Entorno**

```bash
# Redis para WebSocket y cache
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=smarthydro123

# Email para notificaciones
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=notifications@smarthydro.com
```

### **2. Configuración Django**

```python
# settings/base.py

# Django Channels
ASGI_APPLICATION = 'api.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [{
                'host': os.environ.get('REDIS_HOST', 'redis'),
                'port': int(os.environ.get('REDIS_PORT', 6379)),
                'password': os.environ.get('REDIS_PASSWORD', 'smarthydro123'),
            }],
        },
    },
}

# Configuración de notificaciones
NOTIFICATION_SETTINGS = {
    'ENABLE_REALTIME': True,
    'ENABLE_EMAIL': True,
    'DEFAULT_CHANNEL': 'general',
}
```

## 🚀 **Uso del Sistema**

### **1. Notificaciones Automáticas**

Las notificaciones se envían automáticamente cuando ocurren eventos en los módulos del ERP:

```python
# Ejemplo: Cuando se crea una transacción bancaria
from api.apps.erp.banking.models import Transaction

# El signal detecta automáticamente y envía notificación
transaction = Transaction.objects.create(
    bank_account=account,
    transaction_type='DEPOSIT',
    amount=1000.00,
    description='Depósito inicial'
)
```

### **2. Notificaciones Manuales**

También puedes enviar notificaciones manualmente:

```python
from api.apps.notifications.services import notification_service

# Enviar notificación personalizada
notification_service.send_notification(
    template_name='custom_alert',
    module='banking',
    users=[user1, user2],
    context_data={
        'account': account,
        'amount': 5000.00,
        'alert_type': 'high_amount'
    },
    priority='high'
)
```

### **3. WebSocket en Frontend**

```javascript
// Conectar a WebSocket de notificaciones
const socket = new WebSocket("ws://localhost:8000/ws/notifications/");

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);

  if (data.type === "notification") {
    // Mostrar notificación
    showNotification(data.subject, data.message, data.priority);
  }
};

// Marcar como leída
socket.send(
  JSON.stringify({
    type: "notification.read",
    notification_id: 123,
  })
);
```

## 📊 **API REST**

### **Endpoints Principales**

```
GET    /notifications/notifications/          # Listar notificaciones
POST   /notifications/notifications/mark_read/ # Marcar como leída
POST   /notifications/notifications/bulk_action/ # Acción masiva
GET    /notifications/notifications/stats/    # Estadísticas
GET    /notifications/notifications/unread_count/ # Conteo no leídas

GET    /notifications/preferences/            # Preferencias
POST   /notifications/preferences/            # Crear preferencia
PUT    /notifications/preferences/{id}/       # Actualizar preferencia

GET    /notifications/templates/              # Plantillas
GET    /notifications/logs/                   # Logs de envío
```

### **Ejemplo de Uso de la API**

```bash
# Obtener notificaciones del usuario
curl -H "Authorization: Token YOUR_TOKEN" \
     http://localhost:8000/notifications/notifications/

# Marcar notificación como leída
curl -X POST \
     -H "Authorization: Token YOUR_TOKEN" \
     http://localhost:8000/notifications/notifications/123/mark_read/

# Obtener estadísticas
curl -H "Authorization: Token YOUR_TOKEN" \
     http://localhost:8000/notifications/notifications/stats/
```

## 🎨 **Personalización de Plantillas**

### **Variables Disponibles**

Cada módulo tiene variables específicas disponibles:

```python
# Banking
{
    'transaction': 'Objeto Transaction',
    'account': 'Objeto BankAccount',
    'amount': 'Monto de la transacción',
    'type': 'Tipo de transacción',
    'date': 'Fecha de la transacción'
}

# Payments
{
    'payment': 'Objeto Payment',
    'project': 'Objeto Project',
    'amount': 'Monto del pago',
    'method': 'Método de pago',
    'date': 'Fecha del pago'
}

# Support
{
    'ticket': 'Objeto Ticket',
    'title': 'Título del ticket',
    'priority': 'Prioridad',
    'department': 'Departamento',
    'project': 'Proyecto relacionado'
}
```

### **Crear Nueva Plantilla**

```python
from api.apps.notifications.models import NotificationTemplate

template = NotificationTemplate.objects.create(
    name='custom_alert',
    module='banking',
    notification_type='both',
    subject='Alerta personalizada - {{ alert_type }}',
    message_template='''
    Se ha detectado una alerta de tipo {{ alert_type }}.

    Detalles:
    - Cuenta: {{ account.name }}
    - Monto: ${{ amount }}
    - Fecha: {{ date }}

    Acción requerida: {{ action_required }}
    ''',
    available_variables={
        'alert_type': 'Tipo de alerta',
        'account': 'Cuenta bancaria',
        'amount': 'Monto involucrado',
        'date': 'Fecha del evento',
        'action_required': 'Acción requerida'
    }
)
```

## ⚙️ **Preferencias de Usuario**

### **Configurar Preferencias**

```python
from api.apps.notifications.models import NotificationPreference

# Configurar preferencias para un usuario
preference = NotificationPreference.objects.create(
    user=user,
    module='banking',
    email_enabled=True,
    websocket_enabled=True,
    settings={
        'min_amount_alert': 1000.00,
        'daily_summary': True,
        'urgent_only': False
    }
)
```

### **Preferencias por Módulo**

Cada usuario puede configurar diferentes preferencias por módulo:

- **Email habilitado/deshabilitado**
- **WebSocket habilitado/deshabilitado**
- **Configuraciones específicas** (montos mínimos, frecuencias, etc.)

## 📈 **Monitoreo y Logs**

### **Logs de Notificaciones**

```python
from api.apps.notifications.models import NotificationLog

# Ver logs de envío
logs = NotificationLog.objects.filter(
    notification__user=user
).order_by('-sent_at')

# Estadísticas de entrega
stats = logs.values('channel', 'status').annotate(
    count=Count('id')
)
```

### **Métricas Disponibles**

- Total de notificaciones enviadas
- Notificaciones por módulo
- Notificaciones por estado (enviada, fallida, leída)
- Notificaciones por prioridad
- Tasa de entrega exitosa
- Tiempo promedio de entrega

## 🔒 **Seguridad**

### **Autenticación**

- Todas las APIs requieren autenticación
- WebSocket requiere autenticación de usuario
- Preferencias son específicas por usuario

### **Autorización**

- Usuarios solo ven sus propias notificaciones
- Preferencias son privadas por usuario
- Logs incluyen información de auditoría

## 🚀 **Despliegue**

### **1. Instalar Dependencias**

```bash
pip install channels==4.0.0 channels-redis==4.1.0 django-redis==5.4.0
```

### **2. Ejecutar Migraciones**

```bash
python manage.py makemigrations notifications
python manage.py migrate
```

### **3. Configurar Redis**

```bash
# Verificar que Redis esté corriendo
redis-cli ping

# Configurar contraseña si es necesario
redis-cli config set requirepass "smarthydro123"
```

### **4. Probar el Sistema**

```bash
# Crear una notificación de prueba
python manage.py shell

from api.apps.notifications.services import notification_service
from api.apps.users.models import User

user = User.objects.first()
notification_service.send_notification(
    template_name='project_created',
    module='projects',
    users=[user],
    context_data={'name': 'Proyecto Test', 'client': 'Cliente Test'},
    priority='medium'
)
```

## 🐛 **Troubleshooting**

### **Problemas Comunes**

1. **WebSocket no conecta**

   - Verificar que Redis esté corriendo
   - Verificar configuración de CHANNEL_LAYERS
   - Revisar logs de Django

2. **Emails no se envían**

   - Verificar configuración de EMAIL\_\*
   - Revisar logs de email en Django
   - Verificar credenciales SMTP

3. **Notificaciones no se crean**
   - Verificar que los signals estén registrados
   - Revisar logs de Django
   - Verificar que las plantillas existan

### **Logs Útiles**

```python
import logging
logger = logging.getLogger('notifications')

# Habilitar logs detallados
logging.getLogger('notifications').setLevel(logging.DEBUG)
```

## 📚 **Referencias**

- [Django Channels Documentation](https://channels.readthedocs.io/)
- [Redis Documentation](https://redis.io/documentation)
- [Django Signals Documentation](https://docs.djangoproject.com/en/stable/topics/signals/)

---

**¡El sistema de notificaciones está listo para usar!** 🎉

Con esta implementación tienes un sistema completo, modular y escalable que cubre todos los módulos de tu ERP SmartHydro.
