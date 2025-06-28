# 🚀 Implementación de Microservicios SmartHydro

## 📋 Resumen

Este documento describe la implementación de la arquitectura de microservicios para SmartHydro, migrando desde la arquitectura monolítica de Django a servicios independientes y escalables.

## 🏗️ Arquitectura

### **Antes (Monolítica)**

```
┌─────────────────────────────────────┐
│           Django Monolítico         │
│  ┌─────────────┐ ┌─────────────┐    │
│  │  Cronjobs   │ │   API REST  │    │
│  │ Telemetría  │ │   Business  │    │
│  │    DGA      │ │   Admin     │    │
│  └─────────────┘ └─────────────┘    │
└─────────────────────────────────────┘
```

### **Después (Microservicios)**

```
┌─────────────────┐ ┌─────────────────┐ ┌─────────┐
│   Telemetry     │ │   Data          │ │   DGA   │
│   Collector     │ │   Processor     │ │Compliance│
│   (FastAPI)     │ │   (FastAPI)     │ │(FastAPI) │
│   Port: 8001    │ │   Port: 8003    │ │Port: 8002│
└─────────────────┘ └─────────────────┘ └─────────┘
         │                       │               │
         ▼                       ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────┐
│   Kafka         │ │   Redis         │ │Analytics│
│   (Message      │ │   (Cache)       │ │ Engine  │
│    Queue)       │ │                 │ │(FastAPI)│
└─────────────────┘ └─────────────────┘ └─────────┘

┌─────────────────────────────────────────────────┐
│              BUSINESS API (DJANGO)              │
│              Port: 8004                         │
│  • Usuarios y Autenticación                    │
│  • Gestión de Clientes                         │
│  • Gestión de Proyectos                        │
│  • Puntos de Captación                         │
│  • Configuraciones                             │
│  • Notificaciones                              │
│  • Admin Panel                                 │
└─────────────────────────────────────────────────┘
```

## 🔄 Migración de Cronjobs

### **Telemetry Collector (FastAPI + Celery)**

**Migra desde:**

- `api/cronjobs/telemetry/twin.py` (cada hora)
- `api/cronjobs/telemetry/twin_f1.py` (cada minuto)
- `api/cronjobs/telemetry/twin_f5.py` (cada 5 minutos)
- `api/cronjobs/telemetry/nettra.py` (cada hora)
- `api/cronjobs/telemetry/nettra_f5.py` (cada 5 minutos)
- `api/cronjobs/telemetry/novus.py` (cada hora)

**Nueva implementación:**

```python
# services/telemetry-collector/celery_app.py
app.conf.beat_schedule = {
    'collect-twin-1min': {
        'task': 'app.tasks.collect_twin_data',
        'schedule': crontab(minute='*'),
        'args': ('1',),
    },
    'collect-twin-5min': {
        'task': 'app.tasks.collect_twin_data',
        'schedule': crontab(minute='*/5'),
        'args': ('5',),
    },
    'collect-twin-1hour': {
        'task': 'app.tasks.collect_twin_data',
        'schedule': crontab(minute=0, hour='*'),
        'args': ('60',),
    },
    # ... más tareas
}
```

### **DGA Compliance (FastAPI + Celery)**

**Migra desde:**

- `api/cronjobs/dga/cron_dga.py` (cada 3 minutos)
- `api/cronjobs/dga/send_data_dga.py` (lógica SOAP)

**Nueva implementación:**

```python
# services/dga-compliance/celery_app.py
app.conf.beat_schedule = {
    'send-dga-data': {
        'task': 'app.tasks.send_pending_data',
        'schedule': crontab(minute='*/3'),
    }
}
```

## 🏃‍♂️ Cómo Ejecutar

### **1. Desarrollo Local (Docker Compose)**

```bash
# Clonar repositorio
git clone <repository>
cd stack_dev_sh

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Construir y levantar servicios
docker-compose up -d

# Verificar servicios
./scripts/test-microservices.sh
```

### **2. Verificar Servicios**

```bash
# Health checks
curl http://localhost:8001/health  # Telemetry Collector
curl http://localhost:8002/health  # DGA Compliance
curl http://localhost:8004/health  # Business API

# Métricas
curl http://localhost:8001/metrics
curl http://localhost:8002/metrics
```

### **3. Probar Recolección**

```bash
# Iniciar recolección manual
curl -X POST http://localhost:8001/collect/twin
curl -X POST http://localhost:8001/collect/nettra
curl -X POST http://localhost:8001/collect/novus

# Enviar datos a DGA
curl -X POST http://localhost:8002/send-pending-data
```

## 📁 Estructura de Archivos

```
stack_dev_sh/
├── api/                           # 🟢 DJANGO (Business API)
│   ├── core/
│   │   ├── models/               # Usuarios, Clientes, Proyectos
│   │   ├── views/                # API REST
│   │   ├── admin.py              # Admin Panel
│   │   └── ...
│   └── ...
├── services/                      # 🔴 MICROSERVICIOS
│   ├── telemetry-collector/      # FastAPI + Celery
│   │   ├── app/
│   │   │   ├── main.py           # FastAPI app
│   │   │   ├── collectors/       # Proveedores (Twin, Nettra, Novus)
│   │   │   ├── tasks.py          # Tareas Celery
│   │   │   └── ...
│   │   ├── celery_app.py         # Configuración Celery
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── dga-compliance/           # FastAPI + Celery
│   │   ├── app/
│   │   │   ├── main.py           # FastAPI app
│   │   │   ├── senders/          # Cliente SOAP DGA
│   │   │   └── ...
│   │   ├── celery_app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── data-processor/           # TODO: Implementar
│   └── analytics-engine/         # TODO: Implementar
├── docker-compose.yml            # Desarrollo local
├── k8s/                         # Kubernetes (Producción)
└── scripts/
    └── test-microservices.sh    # Script de pruebas
```

## 🔧 Configuración

### **Variables de Entorno**

```bash
# .env
# Base de datos
POSTGRES_PASSWORD=smarthydro123
MONGO_PASSWORD=smarthydro123
REDIS_PASSWORD=smarthydro123

# APIs de proveedores
TWIN_API_KEY=your_twin_api_key
NETTRA_API_KEY=your_nettra_api_key
NOVUS_API_KEY=your_novus_api_key

# DGA
DGA_API_URL=https://snia.mop.gob.cl/controlextraccion/datosExtraccion/SendDataExtraccionService
DGA_API_KEY=your_dga_api_key

# Django
SECRET_KEY=your-secret-key-here
```

### **Puertos de Servicios**

| Servicio            | Puerto | Descripción             |
| ------------------- | ------ | ----------------------- |
| Business API        | 8004   | Django (Gestión)        |
| Telemetry Collector | 8001   | FastAPI (Recolección)   |
| DGA Compliance      | 8002   | FastAPI (Envío DGA)     |
| Data Processor      | 8003   | FastAPI (Procesamiento) |
| Analytics Engine    | 8005   | FastAPI (Analytics)     |
| PostgreSQL          | 5432   | Base de datos           |
| Redis               | 6379   | Cache                   |
| Kafka               | 29092  | Message queue           |
| MongoDB             | 27017  | Analytics DB            |

## 🚀 Escalabilidad

### **Docker Compose (Desarrollo)**

```yaml
# docker-compose.yml
telemetry-collector:
  deploy:
    resources:
      limits:
        cpus: "2"
        memory: 4G
      reservations:
        cpus: "1"
        memory: 2G
```

### **Kubernetes (Producción)**

```yaml
# k8s/hpa/telemetry-collector-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

## 📊 Monitoreo

### **Health Checks**

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "telemetry-collector",
        "timestamp": datetime.now(CHILE_TZ).isoformat(),
        "version": "1.0.0"
    }
```

### **Métricas**

```python
@app.get("/metrics")
async def get_metrics():
    return {
        "service": "telemetry-collector",
        "providers": ["twin", "nettra", "novus"],
        "supported_frequencies": ["1", "5", "60"]
    }
```

## 🔄 Flujo de Datos

### **1. Recolección**

```
Proveedores (Twin/Nettra/Novus)
    ↓
Telemetry Collector (FastAPI)
    ↓
Kafka Topic: measurements
    ↓
Data Processor (FastAPI)
    ↓
Kafka Topic: dga_compliance
    ↓
DGA Compliance (FastAPI)
    ↓
DGA API (SOAP)
```

### **2. Gestión**

```
Business API (Django)
    ↓
Admin Panel / API REST
    ↓
Configuración de puntos
    ↓
Telemetry Collector (consulta configuración)
```

## 🧪 Testing

### **Script de Pruebas**

```bash
# Ejecutar pruebas completas
./scripts/test-microservices.sh

# Ver logs en tiempo real
./scripts/test-microservices.sh --logs
```

### **Pruebas Manuales**

```bash
# Probar recolección
curl -X POST http://localhost:8001/collect/twin

# Probar envío DGA
curl -X POST http://localhost:8002/send-pending-data

# Verificar logs
docker-compose logs -f telemetry-collector
```

## 🚨 Troubleshooting

### **Problemas Comunes**

1. **Servicio no responde**

   ```bash
   # Verificar logs
   docker-compose logs [servicio]

   # Reiniciar servicio
   docker-compose restart [servicio]
   ```

2. **Error de conexión a Django**

   ```bash
   # Verificar que Business API esté corriendo
   curl http://localhost:8004/health

   # Verificar variables de entorno
   docker-compose exec [servicio] env | grep DJANGO_API_URL
   ```

3. **Error de Celery**

   ```bash
   # Verificar workers
   docker-compose logs telemetry-worker
   docker-compose logs dga-worker

   # Reiniciar workers
   docker-compose restart telemetry-worker dga-worker
   ```

## 📈 Próximos Pasos

### **Fase 1: Completar Migración** ✅

- [x] Telemetry Collector
- [x] DGA Compliance
- [ ] Data Processor
- [ ] Analytics Engine

### **Fase 2: Optimizaciones**

- [ ] Implementar colectores reales (Twin, Nettra, Novus)
- [ ] Optimizar procesamiento de datos
- [ ] Implementar analytics avanzados
- [ ] Configurar alertas automáticas

### **Fase 3: Producción**

- [ ] Configurar Kubernetes
- [ ] Implementar CI/CD
- [ ] Configurar monitoreo completo
- [ ] Documentación de API

## 🤝 Contribución

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/smarthydro/issues)
- **Documentación**: [docs/](docs/)
- **Email**: felipebarraza@smarthydro.cl

---

**¡SmartHydro Microservicios está listo para escalar! 🚀**
