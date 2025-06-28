# Migración a Kubernetes

## 🎯 **Visión General**

Esta guía te ayudará a migrar SmartHydro de Docker Compose a Kubernetes, preparándolo para producción con alta disponibilidad, auto-scaling y gestión de recursos avanzada.

## 🏗️ **Arquitectura Kubernetes**

### **Namespaces**

```yaml
# k8s/namespaces.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: smarthydro
  labels:
    name: smarthydro
    environment: production
---
apiVersion: v1
kind: Namespace
metadata:
  name: smarthydro-monitoring
  labels:
    name: smarthydro-monitoring
    environment: production
```

### **ConfigMaps y Secrets**

```yaml
# k8s/config/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: smarthydro-config
  namespace: smarthydro
data:
  DATABASE_URL: "postgresql://smarthydro:$(POSTGRES_PASSWORD)@postgres-service:5432/smarthydro_business"
  REDIS_URL: "redis://redis-service:6379"
  KAFKA_BROKERS: "kafka-service:9092"
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"
---
# k8s/config/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: smarthydro-secrets
  namespace: smarthydro
type: Opaque
data:
  POSTGRES_PASSWORD: <base64-encoded-password>
  MONGO_PASSWORD: <base64-encoded-password>
  JWT_SECRET_KEY: <base64-encoded-secret>
  TWIN_API_KEY: <base64-encoded-key>
  NETTRA_API_KEY: <base64-encoded-key>
  NOVUS_API_KEY: <base64-encoded-key>
  DGA_API_KEY: <base64-encoded-key>
```

## 🚀 **Deployments**

### **Telemetry Collector Deployment**

```yaml
# k8s/deployments/telemetry-collector.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: telemetry-collector
  namespace: smarthydro
  labels:
    app: telemetry-collector
    version: v1.0.0
spec:
  replicas: 3
  selector:
    matchLabels:
      app: telemetry-collector
  template:
    metadata:
      labels:
        app: telemetry-collector
        version: v1.0.0
    spec:
      containers:
        - name: telemetry-collector
          image: smarthydro/telemetry-collector:latest
          ports:
            - containerPort: 8001
          env:
            - name: DATABASE_URL
              valueFrom:
                configMapKeyRef:
                  name: smarthydro-config
                  key: DATABASE_URL
            - name: REDIS_URL
              valueFrom:
                configMapKeyRef:
                  name: smarthydro-config
                  key: REDIS_URL
            - name: KAFKA_BROKERS
              valueFrom:
                configMapKeyRef:
                  name: smarthydro-config
                  key: KAFKA_BROKERS
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: smarthydro-secrets
                  key: POSTGRES_PASSWORD
            - name: TWIN_API_KEY
              valueFrom:
                secretKeyRef:
                  name: smarthydro-secrets
                  key: TWIN_API_KEY
          resources:
            requests:
              memory: "2Gi"
              cpu: "1"
            limits:
              memory: "4Gi"
              cpu: "2"
          livenessProbe:
            httpGet:
              path: /health
              port: 8001
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8001
            initialDelaySeconds: 5
            periodSeconds: 5
          volumeMounts:
            - name: config-volume
              mountPath: /app/config
      volumes:
        - name: config-volume
          configMap:
            name: smarthydro-config
---
apiVersion: v1
kind: Service
metadata:
  name: telemetry-collector-service
  namespace: smarthydro
spec:
  selector:
    app: telemetry-collector
  ports:
    - protocol: TCP
      port: 8001
      targetPort: 8001
  type: ClusterIP
```

### **Business API Deployment**

```yaml
# k8s/deployments/business-api.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: business-api
  namespace: smarthydro
  labels:
    app: business-api
    version: v1.0.0
spec:
  replicas: 2
  selector:
    matchLabels:
      app: business-api
  template:
    metadata:
      labels:
        app: business-api
        version: v1.0.0
    spec:
      containers:
        - name: business-api
          image: smarthydro/business-api:latest
          ports:
            - containerPort: 8004
          env:
            - name: DATABASE_URL
              valueFrom:
                configMapKeyRef:
                  name: smarthydro-config
                  key: DATABASE_URL
            - name: REDIS_URL
              valueFrom:
                configMapKeyRef:
                  name: smarthydro-config
                  key: REDIS_URL
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: smarthydro-secrets
                  key: POSTGRES_PASSWORD
            - name: JWT_SECRET_KEY
              valueFrom:
                secretKeyRef:
                  name: smarthydro-secrets
                  key: JWT_SECRET_KEY
          resources:
            requests:
              memory: "1Gi"
              cpu: "0.5"
            limits:
              memory: "2Gi"
              cpu: "1"
          livenessProbe:
            httpGet:
              path: /health
              port: 8004
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8004
            initialDelaySeconds: 5
            periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: business-api-service
  namespace: smarthydro
spec:
  selector:
    app: business-api
  ports:
    - protocol: TCP
      port: 8004
      targetPort: 8004
  type: ClusterIP
```

## 📊 **StatefulSets para Bases de Datos**

### **PostgreSQL StatefulSet**

```yaml
# k8s/statefulsets/postgres.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: smarthydro
spec:
  serviceName: postgres-service
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:15-alpine
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_DB
              value: "smarthydro_business"
            - name: POSTGRES_USER
              value: "smarthydro"
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: smarthydro-secrets
                  key: POSTGRES_PASSWORD
          volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql/data
          resources:
            requests:
              memory: "2Gi"
              cpu: "1"
            limits:
              memory: "4Gi"
              cpu: "2"
          livenessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - smarthydro
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - smarthydro
            initialDelaySeconds: 5
            periodSeconds: 5
  volumeClaimTemplates:
    - metadata:
        name: postgres-storage
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 100Gi
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: smarthydro
spec:
  selector:
    app: postgres
  ports:
    - protocol: TCP
      port: 5432
      targetPort: 5432
  type: ClusterIP
```

### **Redis StatefulSet**

```yaml
# k8s/statefulsets/redis.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
  namespace: smarthydro
spec:
  serviceName: redis-service
  replicas: 3
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
        - name: redis
          image: redis:7-alpine
          command:
            ["redis-server", "--appendonly", "yes", "--cluster-enabled", "yes"]
          ports:
            - containerPort: 6379
          volumeMounts:
            - name: redis-storage
              mountPath: /data
          resources:
            requests:
              memory: "1Gi"
              cpu: "0.5"
            limits:
              memory: "2Gi"
              cpu: "1"
          livenessProbe:
            exec:
              command:
                - redis-cli
                - ping
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - redis-cli
                - ping
            initialDelaySeconds: 5
            periodSeconds: 5
  volumeClaimTemplates:
    - metadata:
        name: redis-storage
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 20Gi
---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
  namespace: smarthydro
spec:
  selector:
    app: redis
  ports:
    - protocol: TCP
      port: 6379
      targetPort: 6379
  type: ClusterIP
```

## 🔄 **Horizontal Pod Autoscaler**

### **HPA para Telemetry Collector**

```yaml
# k8s/hpa/telemetry-collector-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: telemetry-collector-hpa
  namespace: smarthydro
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: telemetry-collector
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
```

### **HPA para Business API**

```yaml
# k8s/hpa/business-api-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: business-api-hpa
  namespace: smarthydro
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: business-api
  minReplicas: 2
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

## 🌐 **Ingress y Load Balancer**

### **Ingress Controller**

```yaml
# k8s/ingress/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: smarthydro-ingress
  namespace: smarthydro
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "30"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "600"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "600"
spec:
  tls:
    - hosts:
        - api.smarthydro.com
        - telemetry.smarthydro.com
      secretName: smarthydro-tls
  rules:
    - host: api.smarthydro.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: business-api-service
                port:
                  number: 8004
    - host: telemetry.smarthydro.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: telemetry-collector-service
                port:
                  number: 8001
```

## 📊 **Monitoring y Logging**

### **Prometheus Deployment**

```yaml
# k8s/monitoring/prometheus.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
  namespace: smarthydro-monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
        - name: prometheus
          image: prom/prometheus:latest
          ports:
            - containerPort: 9090
          volumeMounts:
            - name: prometheus-config
              mountPath: /etc/prometheus
            - name: prometheus-storage
              mountPath: /prometheus
          command:
            - /bin/prometheus
            - --config.file=/etc/prometheus/prometheus.yml
            - --storage.tsdb.path=/prometheus
            - --web.console.libraries=/etc/prometheus/console_libraries
            - --web.console.templates=/etc/prometheus/consoles
            - --storage.tsdb.retention.time=200h
            - --web.enable-lifecycle
          resources:
            requests:
              memory: "1Gi"
              cpu: "0.5"
            limits:
              memory: "2Gi"
              cpu: "1"
      volumes:
        - name: prometheus-config
          configMap:
            name: prometheus-config
        - name: prometheus-storage
          persistentVolumeClaim:
            claimName: prometheus-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: prometheus-service
  namespace: smarthydro-monitoring
spec:
  selector:
    app: prometheus
  ports:
    - protocol: TCP
      port: 9090
      targetPort: 9090
  type: ClusterIP
```

### **Grafana Deployment**

```yaml
# k8s/monitoring/grafana.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
  namespace: smarthydro-monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      containers:
        - name: grafana
          image: grafana/grafana:latest
          ports:
            - containerPort: 3000
          env:
            - name: GF_SECURITY_ADMIN_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: smarthydro-secrets
                  key: GRAFANA_PASSWORD
          volumeMounts:
            - name: grafana-storage
              mountPath: /var/lib/grafana
          resources:
            requests:
              memory: "512Mi"
              cpu: "0.25"
            limits:
              memory: "1Gi"
              cpu: "0.5"
      volumes:
        - name: grafana-storage
          persistentVolumeClaim:
            claimName: grafana-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: grafana-service
  namespace: smarthydro-monitoring
spec:
  selector:
    app: grafana
  ports:
    - protocol: TCP
      port: 3000
      targetPort: 3000
  type: ClusterIP
```

## 🔧 **Scripts de Despliegue**

### **Script de Despliegue Completo**

```bash
#!/bin/bash
# scripts/deploy-k8s.sh

echo "🚀 Desplegando SmartHydro en Kubernetes..."

# Verificar kubectl
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl no está instalado"
    exit 1
fi

# Verificar contexto
echo "🔍 Verificando contexto de Kubernetes..."
kubectl cluster-info

# Crear namespaces
echo "📦 Creando namespaces..."
kubectl apply -f k8s/namespaces.yaml

# Aplicar configuraciones
echo "⚙️  Aplicando configuraciones..."
kubectl apply -f k8s/config/

# Desplegar bases de datos
echo "🗄️  Desplegando bases de datos..."
kubectl apply -f k8s/statefulsets/

# Esperar a que las bases de datos estén listas
echo "⏳ Esperando a que las bases de datos estén listas..."
kubectl wait --for=condition=ready pod -l app=postgres -n smarthydro --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis -n smarthydro --timeout=300s

# Desplegar microservicios
echo "🔧 Desplegando microservicios..."
kubectl apply -f k8s/deployments/

# Aplicar HPA
echo "📈 Aplicando auto-scaling..."
kubectl apply -f k8s/hpa/

# Desplegar monitoring
echo "📊 Desplegando monitoring..."
kubectl apply -f k8s/monitoring/

# Aplicar ingress
echo "🌐 Configurando ingress..."
kubectl apply -f k8s/ingress/

# Verificar despliegue
echo "🔍 Verificando despliegue..."
kubectl get pods -n smarthydro
kubectl get pods -n smarthydro-monitoring

echo "✅ SmartHydro desplegado exitosamente!"
echo "📊 Grafana: http://localhost:3000"
echo "📈 Prometheus: http://localhost:9090"
echo "🔌 Business API: http://api.smarthydro.com"
echo "📡 Telemetry Collector: http://telemetry.smarthydro.com"
```

### **Script de Rollback**

```bash
#!/bin/bash
# scripts/rollback-k8s.sh

echo "🔄 Haciendo rollback de SmartHydro..."

# Obtener versión anterior
PREVIOUS_VERSION=$(kubectl get deployment telemetry-collector -n smarthydro -o jsonpath='{.metadata.annotations.previous-version}')

if [ -z "$PREVIOUS_VERSION" ]; then
    echo "❌ No se encontró versión anterior"
    exit 1
fi

echo "📦 Haciendo rollback a versión $PREVIOUS_VERSION..."

# Rollback de deployments
kubectl rollout undo deployment/telemetry-collector -n smarthydro
kubectl rollout undo deployment/business-api -n smarthydro

# Verificar rollback
kubectl rollout status deployment/telemetry-collector -n smarthydro
kubectl rollout status deployment/business-api -n smarthydro

echo "✅ Rollback completado"
```

## 📚 **Comandos Útiles**

### **Gestión de Pods**

```bash
# Ver pods
kubectl get pods -n smarthydro

# Ver logs
kubectl logs -f deployment/telemetry-collector -n smarthydro

# Ejecutar comando en pod
kubectl exec -it deployment/telemetry-collector -n smarthydro -- /bin/bash

# Escalar deployment
kubectl scale deployment telemetry-collector --replicas=5 -n smarthydro
```

### **Monitoreo**

```bash
# Ver métricas
kubectl top pods -n smarthydro

# Ver HPA
kubectl get hpa -n smarthydro

# Ver servicios
kubectl get svc -n smarthydro

# Ver ingress
kubectl get ingress -n smarthydro
```

### **Troubleshooting**

```bash
# Describir pod
kubectl describe pod <pod-name> -n smarthydro

# Ver eventos
kubectl get events -n smarthydro --sort-by='.lastTimestamp'

# Ver logs de todos los contenedores
kubectl logs deployment/telemetry-collector -n smarthydro --all-containers
```

## 🎯 **Próximos Pasos**

1. **Configurar cluster Kubernetes**
2. **Instalar Helm y charts**
3. **Configurar CI/CD pipeline**
4. **Implementar backup automático**
5. **Configurar alertas**
6. **Optimizar recursos**
7. **Implementar blue-green deployment**

## 📖 **Recursos de Aprendizaje**

### **Kubernetes**

- [Kubernetes.io](https://kubernetes.io/)
- [Kubernetes by Example](https://kubernetesbyexample.com/)

### **Helm**

- [Helm.sh](https://helm.sh/)
- [Helm Charts](https://artifacthub.io/)

### **Monitoring**

- [Prometheus Operator](https://prometheus-operator.dev/)
- [Grafana Operator](https://grafana.com/docs/grafana/latest/setup-grafana/installation/kubernetes/)

### **CI/CD**

- [ArgoCD](https://argoproj.github.io/argo-cd/)
- [Flux](https://fluxcd.io/)
