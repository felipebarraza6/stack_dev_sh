#!/bin/bash

# SmartHydro Kubernetes Deployment Script
# Este script despliega SmartHydro en Kubernetes

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_message() {
    echo -e "${BLUE}[SmartHydro K8s]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SmartHydro K8s]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[SmartHydro K8s]${NC} $1"
}

print_error() {
    echo -e "${RED}[SmartHydro K8s]${NC} $1"
}

print_message "🚀 Desplegando SmartHydro en Kubernetes..."

# Verificar kubectl
if ! command -v kubectl &> /dev/null; then
    print_error "❌ kubectl no está instalado"
    print_message "Por favor, instala kubectl desde: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

# Verificar contexto
print_message "🔍 Verificando contexto de Kubernetes..."
kubectl cluster-info

if [ $? -ne 0 ]; then
    print_error "❌ No se pudo conectar al cluster de Kubernetes"
    print_message "Verifica que tu cluster esté corriendo y el contexto esté configurado"
    exit 1
fi

print_success "✅ Conectado al cluster de Kubernetes"

# Verificar namespace
print_message "📦 Verificando namespaces..."
kubectl get namespaces | grep smarthydro || true

# Crear namespaces
print_message "📦 Creando namespaces..."
kubectl apply -f k8s/namespaces.yaml

# Aplicar configuraciones
print_message "⚙️  Aplicando configuraciones..."
kubectl apply -f k8s/config/

# Crear Persistent Volumes
print_message "💾 Creando Persistent Volumes..."
kubectl apply -f k8s/storage/

# Desplegar bases de datos
print_message "🗄️  Desplegando bases de datos..."
kubectl apply -f k8s/statefulsets/

# Esperar a que las bases de datos estén listas
print_message "⏳ Esperando a que las bases de datos estén listas..."
kubectl wait --for=condition=ready pod -l app=postgres -n smarthydro --timeout=300s
kubectl wait --for=condition=ready pod -l app=mongodb -n smarthydro --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis -n smarthydro --timeout=300s

# Desplegar microservicios
print_message "🔧 Desplegando microservicios..."
kubectl apply -f k8s/deployments/

# Aplicar HPA
print_message "📈 Aplicando auto-scaling..."
kubectl apply -f k8s/hpa/

# Desplegar monitoring
print_message "📊 Desplegando monitoring..."
kubectl apply -f k8s/monitoring/

# Aplicar ingress
print_message "🌐 Configurando ingress..."
kubectl apply -f k8s/ingress/

# Verificar despliegue
print_message "🔍 Verificando despliegue..."
kubectl get pods -n smarthydro
kubectl get pods -n smarthydro-monitoring

# Verificar servicios
print_message "🔍 Verificando servicios..."
kubectl get svc -n smarthydro
kubectl get svc -n smarthydro-monitoring

# Verificar ingress
print_message "🔍 Verificando ingress..."
kubectl get ingress -n smarthydro-ingress

# Mostrar información de acceso
echo
print_success "🎉 SmartHydro desplegado exitosamente!"
echo
echo -e "${GREEN}📊 Dashboards y Monitoreo:${NC}"
echo -e "   Grafana:     ${BLUE}http://grafana.smarthydro.com${NC}"
echo -e "   Prometheus:  ${BLUE}http://prometheus.smarthydro.com${NC}"
echo
echo -e "${GREEN}🔌 APIs:${NC}"
echo -e "   Business API:        ${BLUE}https://api.smarthydro.com${NC}"
echo -e "   Telemetry Collector: ${BLUE}https://telemetry.smarthydro.com${NC}"
echo -e "   Analytics Engine:    ${BLUE}https://analytics.smarthydro.com${NC}"
echo -e "   DGA Compliance:      ${BLUE}https://dga.smarthydro.com${NC}"
echo
echo -e "${GREEN}📋 Comandos Útiles:${NC}"
echo -e "   Ver pods:           ${BLUE}kubectl get pods -n smarthydro${NC}"
echo -e "   Ver logs:           ${BLUE}kubectl logs -f deployment/telemetry-collector -n smarthydro${NC}"
echo -e "   Escalar servicio:   ${BLUE}kubectl scale deployment telemetry-collector --replicas=5 -n smarthydro${NC}"
echo -e "   Ver HPA:            ${BLUE}kubectl get hpa -n smarthydro${NC}"
echo -e "   Ver métricas:       ${BLUE}kubectl top pods -n smarthydro${NC}"
echo

print_success "🎯 SmartHydro desplegado en Kubernetes!"
print_message "💡 Para ver logs: kubectl logs -f deployment/telemetry-collector -n smarthydro"
print_message "💡 Para escalar: kubectl scale deployment telemetry-collector --replicas=5 -n smarthydro" 