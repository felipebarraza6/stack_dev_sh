# Configuración Docker para SmartHydro

## 🎯 **Visión General**

Esta guía te ayudará a configurar SmartHydro en tu Mac usando Docker. La configuración está optimizada para desarrollo local con alta performance y escalabilidad.

## 🏗️ **Estructura Docker**

### **Servicios Principales**

```yaml
# docker-compose.yml
services:
  # Base de datos
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: smarthydro_business
      POSTGRES_USER: smarthydro
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U smarthydro"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Cache y Message Broker
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Message Queue
  kafka:
    image: confluentinc/cp-kafka:7.4.0
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    ports:
      - "9092:9092"
    depends_on:
      - zookeeper

  zookeeper:
    image: confluentinc/cp-zookeeper:7.4.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  # Base de datos para mediciones
  mongodb:
    image: mongo:6.0
    environment:
      MONGO_INITDB_ROOT_USERNAME: smarthydro
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD}
      MONGO_INITDB_DATABASE: smarthydro_measurements
    volumes:
      - mongodb_data:/data/db
    ports:
      - "27017:27017"
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Microservicios
  telemetry-collector:
    build:
      context: ./services/telemetry-collector
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://smarthydro:${POSTGRES_PASSWORD}@postgres:5432/smarthydro_business
      - REDIS_URL=redis://redis:6379
      - KAFKA_BROKERS=kafka:9092
    ports:
      - "8001:8001"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      kafka:
        condition: service_started
    deploy:
      resources:
        limits:
          cpus: "2"
          memory: 4G
        reservations:
          cpus: "1"
          memory: 2G

  business-api:
    build:
      context: ./services/business-api
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://smarthydro:${POSTGRES_PASSWORD}@postgres:5432/smarthydro_business
      - REDIS_URL=redis://redis:6379
    ports:
      - "8004:8004"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    deploy:
      resources:
        limits:
          cpus: "1"
          memory: 2G
        reservations:
          cpus: "0.5"
          memory: 1G

  # Monitoring
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.path=/prometheus"
      - "--web.console.libraries=/etc/prometheus/console_libraries"
      - "--web.console.templates=/etc/prometheus/consoles"
      - "--storage.tsdb.retention.time=200h"
      - "--web.enable-lifecycle"

  grafana:
    image: grafana/grafana:latest
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

volumes:
  postgres_data:
  redis_data:
  mongodb_data:
  prometheus_data:
  grafana_data:
```

## 🔧 **Configuración de Variables de Entorno**

### **Archivo .env**

```bash
# .env
# Base de datos
POSTGRES_PASSWORD=your_secure_password_here
MONGO_PASSWORD=your_mongo_password_here

# Redis
REDIS_PASSWORD=your_redis_password_here

# Kafka
KAFKA_TOPIC_MEASUREMENTS=measurements
KAFKA_TOPIC_NOTIFICATIONS=notifications

# API Keys
TWIN_API_KEY=your_twin_api_key
NETTRA_API_KEY=your_nettra_api_key
NOVUS_API_KEY=your_novus_api_key

# Monitoring
GRAFANA_PASSWORD=your_grafana_password

# JWT
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs
DGA_API_URL=https://api.dga.cl
DGA_API_KEY=your_dga_api_key
```

## 🚀 **Scripts de Despliegue**

### **Script de Inicio**

```bash
#!/bin/bash
# scripts/start.sh

echo "🚀 Iniciando SmartHydro Microservices..."

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado"
    exit 1
fi

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env..."
    cp .env.example .env
    echo "⚠️  Por favor, edita el archivo .env con tus credenciales"
    exit 1
fi

# Construir imágenes
echo "🔨 Construyendo imágenes Docker..."
docker-compose build

# Iniciar servicios
echo "🚀 Iniciando servicios..."
docker-compose up -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 30

# Verificar health checks
echo "🔍 Verificando health checks..."
docker-compose ps

# Mostrar logs
echo "📋 Mostrando logs..."
docker-compose logs --tail=50

echo "✅ SmartHydro está listo!"
echo "📊 Grafana: http://localhost:3000"
echo "📈 Prometheus: http://localhost:9090"
echo "🔌 Business API: http://localhost:8004"
echo "📡 Telemetry Collector: http://localhost:8001"
```

### **Script de Parada**

```bash
#!/bin/bash
# scripts/stop.sh

echo "🛑 Deteniendo SmartHydro..."

# Detener servicios
docker-compose down

echo "✅ Servicios detenidos"
```

### **Script de Limpieza**

```bash
#!/bin/bash
# scripts/clean.sh

echo "🧹 Limpiando SmartHydro..."

# Detener y eliminar contenedores
docker-compose down -v

# Eliminar imágenes
docker-compose down --rmi all

# Eliminar volúmenes
docker volume prune -f

echo "✅ Limpieza completada"
```

## 📊 **Dockerfiles Optimizados**

### **Telemetry Collector Dockerfile**

```dockerfile
# services/telemetry-collector/Dockerfile
FROM python:3.11-slim

# Crear usuario no-root
RUN groupadd -r smarthydro && useradd -r -g smarthydro smarthydro

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Cambiar permisos
RUN chown -R smarthydro:smarthydro /app

# Cambiar a usuario no-root
USER smarthydro

# Exponer puerto
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Comando de inicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "4"]
```

### **Business API Dockerfile**

```dockerfile
# services/business-api/Dockerfile
FROM python:3.11-slim

# Crear usuario no-root
RUN groupadd -r smarthydro && useradd -r -g smarthydro smarthydro

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Cambiar permisos
RUN chown -R smarthydro:smarthydro /app

# Cambiar a usuario no-root
USER smarthydro

# Exponer puerto
EXPOSE 8004

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8004/health || exit 1

# Comando de inicio
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8004", "--workers", "4", "--worker-class", "gevent"]
```

## 🔍 **Monitoreo y Logs**

### **Configuración de Prometheus**

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "telemetry-collector"
    static_configs:
      - targets: ["telemetry-collector:8001"]
    metrics_path: "/metrics"

  - job_name: "business-api"
    static_configs:
      - targets: ["business-api:8004"]
    metrics_path: "/metrics"

  - job_name: "postgres"
    static_configs:
      - targets: ["postgres:5432"]

  - job_name: "redis"
    static_configs:
      - targets: ["redis:6379"]
```

### **Dashboard de Grafana**

```json
{
  "dashboard": {
    "title": "SmartHydro Overview",
    "panels": [
      {
        "title": "Provider Health",
        "type": "stat",
        "targets": [
          {
            "expr": "provider_health_status",
            "legendFormat": "{{provider}}"
          }
        ]
      },
      {
        "title": "Data Collection Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(provider_requests_total[5m])",
            "legendFormat": "{{provider}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(provider_response_time_seconds_bucket[5m]))",
            "legendFormat": "{{provider}}"
          }
        ]
      }
    ]
  }
}
```

## 🚀 **Comandos Útiles**

### **Iniciar Servicios**

```bash
# Iniciar todos los servicios
docker-compose up -d

# Iniciar solo base de datos
docker-compose up -d postgres redis mongodb

# Iniciar con logs
docker-compose up
```

### **Ver Logs**

```bash
# Ver logs de todos los servicios
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs telemetry-collector

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de los últimos 100 líneas
docker-compose logs --tail=100
```

### **Gestión de Servicios**

```bash
# Reiniciar un servicio
docker-compose restart telemetry-collector

# Parar un servicio
docker-compose stop business-api

# Iniciar un servicio
docker-compose start business-api

# Reconstruir un servicio
docker-compose up -d --build telemetry-collector
```

### **Base de Datos**

```bash
# Conectar a PostgreSQL
docker-compose exec postgres psql -U smarthydro -d smarthydro_business

# Conectar a MongoDB
docker-compose exec mongodb mongosh -u smarthydro -p

# Conectar a Redis
docker-compose exec redis redis-cli
```

### **Monitoreo**

```bash
# Ver uso de recursos
docker stats

# Ver procesos
docker-compose ps

# Ver health checks
docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
```

## 🔧 **Troubleshooting**

### **Problemas Comunes**

#### **1. Puerto ya en uso**

```bash
# Ver qué está usando el puerto
lsof -i :8001

# Matar proceso
kill -9 <PID>
```

#### **2. Problemas de memoria**

```bash
# Ver uso de memoria
docker stats

# Limpiar recursos no usados
docker system prune -a
```

#### **3. Problemas de red**

```bash
# Ver redes Docker
docker network ls

# Inspeccionar red
docker network inspect smarthydro_default
```

#### **4. Problemas de permisos**

```bash
# Cambiar permisos de volúmenes
sudo chown -R $USER:$USER ./data
```

## 📚 **Recursos de Aprendizaje**

### **Docker**

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### **Kubernetes**

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Minikube](https://minikube.sigs.k8s.io/)

### **Monitoring**

- [Prometheus](https://prometheus.io/docs/)
- [Grafana](https://grafana.com/docs/)

### **Message Queues**

- [Apache Kafka](https://kafka.apache.org/documentation/)
- [Redis](https://redis.io/documentation/)
