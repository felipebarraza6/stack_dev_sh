# Sistema de Monitoreo - Grafana + Prometheus

## Descripción General

El sistema de monitoreo integra **Grafana** y **Prometheus** para proporcionar visualización en tiempo real, alertas automáticas y métricas detalladas del sistema de telemetría.

## Componentes del Stack

### 1. Prometheus

- **Función**: Recolector y almacenamiento de métricas
- **Puerto**: 9090
- **Retención**: 200 horas de datos
- **Configuración**: `monitoring/prometheus/prometheus.yml`

### 2. Grafana

- **Función**: Visualización y dashboards
- **Puerto**: 3000
- **Credenciales**: admin/admin123
- **Dashboards**: Automáticamente provisionados

### 3. Alertmanager

- **Función**: Gestión de alertas
- **Puerto**: 9093
- **Notificaciones**: Email, Slack, webhooks

### 4. Exporters

- **Node Exporter**: Métricas del sistema (puerto 9100)
- **PostgreSQL Exporter**: Métricas de base de datos (puerto 9187)
- **Redis Exporter**: Métricas de caché (puerto 9121)
- **Nginx Exporter**: Métricas del proxy (puerto 9113)
- **cAdvisor**: Métricas de contenedores (puerto 8080)

## Métricas de Telemetría

### Métricas Principales

#### Caudal (Flow)

```promql
# Caudal actual por punto
telemetry_flow_litros_segundo{catchment_point="123"}

# Caudal promedio 5 minutos
telemetry_flow_promedio{catchment_point="123"}

# Caudal en 0 (posible falla)
telemetry_flow_litros_segundo == 0
```

#### Nivel Freático (Level)

```promql
# Nivel actual por punto
telemetry_level_metros{catchment_point="123"}

# Nivel promedio 5 minutos
telemetry_level_promedio{catchment_point="123"}

# Nivel crítico (>90m)
telemetry_level_metros > 90
```

#### Totalizado (Total)

```promql
# Total acumulado por punto
telemetry_total_metros_cubicos{catchment_point="123"}

# Inconsistencias detectadas
telemetry_total_inconsistencia > 0
```

#### Conectividad

```promql
# Última medición por punto
telemetry_ultima_medicion{catchment_point="123"}

# Puntos desconectados (>1 hora)
time() - telemetry_ultima_medicion > 3600
```

### Métricas de Sistema

#### Proveedores

```promql
# Errores por proveedor
telemetry_proveedor_errores{proveedor="twin"}

# Éxitos por proveedor
rate(telemetry_proveedor_exitos{proveedor="twin"}[5m])
```

#### Sistema DGA

```promql
# Elementos en cola DGA
telemetry_dga_cola_elementos

# Envíos exitosos a DGA
rate(telemetry_dga_enviados_total{status="success"}[5m])

# Errores de envío DGA
rate(telemetry_dga_errores_envio[5m])
```

#### API

```promql
# Peticiones por minuto
rate(telemetry_api_requests_total[1m])

# Duración P95 de peticiones
histogram_quantile(0.95, rate(telemetry_api_request_duration_seconds_bucket[5m]))

# Errores 5xx
rate(telemetry_api_requests_total{status=~"5.."}[5m])
```

## Alertas Configuradas

### Alertas de Telemetría

#### Caudal

- **CaudalCero**: Alerta si caudal está en 0 por más de 5 minutos
- **CaudalAlto**: Alerta si caudal supera 500 l/s por más de 2 minutos

#### Nivel Freático

- **NivelCritico**: Alerta si nivel supera 90m por más de 1 minuto
- **NivelMaximo**: Alerta si nivel supera 95m por más de 30 segundos

#### Totalizado

- **TotalInconsistente**: Alerta si se detecta inconsistencia entre caudal y total

#### Conectividad

- **PuntoDesconectado**: Alerta si no hay datos por más de 1 hora

### Alertas de Sistema

#### Proveedores

- **ProveedorFallando**: Alerta si un proveedor tiene más de 3 errores en 10 minutos

#### DGA

- **ColaDGALlena**: Alerta si hay más de 100 elementos en cola
- **DGAFallando**: Alerta si hay más de 5 errores de envío en 15 minutos

#### Infraestructura

- **CPUAlto**: Alerta si CPU supera 80%
- **MemoriaAlta**: Alerta si memoria supera 85%
- **DiscoLleno**: Alerta si disco supera 90%

## Dashboards Disponibles

### Dashboard Principal de Telemetría

- **URL**: http://localhost:3000/d/telemetry/main
- **Paneles**:
  1. Puntos de Captación Activos
  2. Caudal Promedio por Punto
  3. Nivel Freático por Punto
  4. Total Acumulado por Punto
  5. Errores por Tipo (gráfico circular)
  6. Estado de Proveedores
  7. Cola DGA
  8. Peticiones API por Minuto
  9. Duración de Peticiones API

### Dashboard de Sistema

- **URL**: http://localhost:3000/d/system/main
- **Paneles**:
  1. Uso de CPU y Memoria
  2. Espacio en Disco
  3. Conexiones de Base de Datos
  4. Métricas de Redis
  5. Métricas de Nginx
  6. Estado de Contenedores

## Instalación y Configuración

### 1. Iniciar Stack de Monitoreo

```bash
# Iniciar solo el stack de monitoreo
docker-compose -f docker-compose.monitoring.yml up -d

# Verificar servicios
docker-compose -f docker-compose.monitoring.yml ps
```

### 2. Configurar Métricas en Django

```python
# En settings.py
INSTALLED_APPS += ['django_prometheus']

MIDDLEWARE = [
    'api.telemetry.metrics.MetricsMiddleware',
    # ... otros middleware
]

# Endpoint de métricas
urlpatterns += [
    path('metrics/', 'api.telemetry.metrics.metrics_view'),
]
```

### 3. Acceder a Grafana

```bash
# URL: http://localhost:3000
# Usuario: admin
# Contraseña: admin123
```

### 4. Configurar Datasource

- Grafana detectará automáticamente Prometheus
- URL: http://prometheus:9090

### 5. Importar Dashboards

- Los dashboards se importan automáticamente
- Ubicación: `monitoring/grafana/dashboards/`

## Configuración de Alertas

### Alertmanager

```yaml
# monitoring/alertmanager/alertmanager.yml
global:
  smtp_smarthost: "smtp.gmail.com:587"
  smtp_from: "alertas@example.com"
  smtp_auth_username: "alertas@example.com"
  smtp_auth_password: "your_password"

route:
  group_by: ["alertname"]
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: "email-alerts"

receivers:
  - name: "email-alerts"
    email_configs:
      - to: "admin@example.com"
```

### Notificaciones por Email

```python
# En api/telemetry/processor.py
def _send_alert_email(self, catchment_point, alerts):
    # Configuración de email para alertas
    send_mail(
        subject=f"Alerta Telemetría - {catchment_point.name}",
        message=alert_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[catchment_point.user.email]
    )
```

## Consultas Útiles

### Puntos con Problemas

```promql
# Puntos con caudal en 0
telemetry_flow_litros_segundo == 0

# Puntos con nivel crítico
telemetry_level_metros > 90

# Puntos desconectados
time() - telemetry_ultima_medicion > 3600
```

### Performance del Sistema

```promql
# API lenta (P95 > 2s)
histogram_quantile(0.95, rate(telemetry_api_request_duration_seconds_bucket[5m])) > 2

# Tasa de errores alta
rate(telemetry_api_requests_total{status=~"5.."}[5m]) > 0.1
```

### Estado de Proveedores

```promql
# Proveedor con más errores
topk(1, sum by (proveedor) (telemetry_proveedor_errores))

# Tasa de éxito por proveedor
rate(telemetry_proveedor_exitos[5m]) / (rate(telemetry_proveedor_exitos[5m]) + rate(telemetry_proveedor_errores[5m]))
```

## Mantenimiento

### Backup de Datos

```bash
# Backup de Prometheus
docker exec prometheus promtool tsdb backup /prometheus /backup

# Backup de Grafana
docker exec grafana grafana-cli admin backup /var/lib/grafana/backup
```

### Limpieza de Datos

```bash
# Limpiar datos antiguos de Prometheus
docker exec prometheus promtool tsdb clean /prometheus --retention.time=200h
```

### Actualización de Configuración

```bash
# Recargar configuración de Prometheus
curl -X POST http://localhost:9090/-/reload

# Recargar configuración de Alertmanager
curl -X POST http://localhost:9093/-/reload
```

## Troubleshooting

### Problemas Comunes

1. **Prometheus no recolecta métricas**

   - Verificar conectividad con Django
   - Revisar logs: `docker logs prometheus`

2. **Grafana no muestra datos**

   - Verificar datasource de Prometheus
   - Revisar consultas PromQL

3. **Alertas no se envían**

   - Verificar configuración de Alertmanager
   - Revisar logs: `docker logs alertmanager`

4. **Métricas no aparecen**
   - Verificar endpoint `/metrics` en Django
   - Revisar configuración de exporters

### Logs Útiles

```bash
# Logs de Prometheus
docker logs prometheus

# Logs de Grafana
docker logs grafana

# Logs de Alertmanager
docker logs alertmanager

# Logs de Django (métricas)
docker logs django
```

## Próximas Mejoras

### Fase 2 del Monitoreo

1. **Alertas Avanzadas**

   - Anomalía detection con ML
   - Alertas predictivas
   - Correlación de eventos

2. **Dashboards Específicos**

   - Dashboard por punto de captación
   - Dashboard de DGA
   - Dashboard de proveedores

3. **Integración Externa**

   - Slack notifications
   - Webhooks personalizados
   - Integración con sistemas de tickets

4. **Métricas de Negocio**
   - KPIs de telemetría
   - Reportes automáticos
   - Análisis de tendencias

---

**Versión**: 1.0.0  
**Última actualización**: 2025-01-24  
**Mantenido por**: Equipo de DevOps
