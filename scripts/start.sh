#!/bin/bash

# SmartHydro Microservices - Script de Inicio
# Este script inicia todos los servicios de SmartHydro

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_message() {
    echo -e "${BLUE}[SmartHydro]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SmartHydro]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[SmartHydro]${NC} $1"
}

print_error() {
    echo -e "${RED}[SmartHydro]${NC} $1"
}

# Banner
echo -e "${BLUE}"
cat << "EOF"
 ____                      _    _           _ 
/ ___|  _ __ ___   __ _  | |  | |_ __   __| |
\___ \ | '_ ` _ \ / _` | | |__| | '_ \ / _` |
 ___) || | | | | | (_| | |  __  | | | | (_| |
|____/ |_| |_| |_|\__,_| |_| |_|_| |_|\__,_|
                                              
Microservices Platform v2.0
EOF
echo -e "${NC}"

print_message "🚀 Iniciando SmartHydro Microservices..."

# Verificar Docker
if ! command -v docker &> /dev/null; then
    print_error "❌ Docker no está instalado"
    print_message "Por favor, instala Docker Desktop desde: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "❌ Docker Compose no está instalado"
    print_message "Por favor, instala Docker Compose"
    exit 1
fi

# Verificar que Docker esté corriendo
if ! docker info &> /dev/null; then
    print_error "❌ Docker no está corriendo"
    print_message "Por favor, inicia Docker Desktop"
    exit 1
fi

print_success "✅ Docker y Docker Compose están disponibles"

# Verificar archivo .env
if [ ! -f .env ]; then
    print_warning "⚠️  Archivo .env no encontrado"
    if [ -f env.example ]; then
        print_message "📝 Copiando archivo de ejemplo..."
        cp env.example .env
        print_warning "⚠️  Por favor, edita el archivo .env con tus credenciales antes de continuar"
        print_message "💡 Puedes usar: nano .env o code .env"
        exit 1
    else
        print_error "❌ No se encontró archivo de ejemplo env.example"
        exit 1
    fi
fi

print_success "✅ Archivo .env encontrado"

# Verificar recursos del sistema
print_message "🔍 Verificando recursos del sistema..."

# Verificar memoria disponible (mínimo 6GB)
MEMORY_GB=$(free -g | awk '/^Mem:/{print $2}')
if [ "$MEMORY_GB" -lt 6 ]; then
    print_warning "⚠️  Memoria insuficiente: ${MEMORY_GB}GB (mínimo 6GB recomendado)"
    print_message "SmartHydro puede funcionar con menos memoria, pero el rendimiento puede verse afectado"
fi

# Verificar espacio en disco (mínimo 10GB)
DISK_GB=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "$DISK_GB" -lt 10 ]; then
    print_warning "⚠️  Espacio en disco insuficiente: ${DISK_GB}GB (mínimo 10GB recomendado)"
fi

print_success "✅ Recursos del sistema verificados"

# Crear directorios necesarios
print_message "📁 Creando directorios necesarios..."
mkdir -p logs
mkdir -p media
mkdir -p config
mkdir -p monitoring/grafana/dashboards
mkdir -p monitoring/grafana/datasources
mkdir -p nginx/conf.d
mkdir -p ssl

# Verificar si los servicios ya están corriendo
if docker-compose ps | grep -q "Up"; then
    print_warning "⚠️  Algunos servicios ya están corriendo"
    read -p "¿Deseas reiniciar todos los servicios? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_message "🛑 Deteniendo servicios existentes..."
        docker-compose down
    else
        print_message "Continuando con servicios existentes..."
    fi
fi

# Construir imágenes
print_message "🔨 Construyendo imágenes Docker..."
docker-compose build --parallel

if [ $? -ne 0 ]; then
    print_error "❌ Error construyendo imágenes"
    exit 1
fi

print_success "✅ Imágenes construidas exitosamente"

# Iniciar servicios base primero
print_message "🚀 Iniciando servicios base..."
docker-compose up -d postgres mongodb redis zookeeper

# Esperar a que las bases de datos estén listas
print_message "⏳ Esperando a que las bases de datos estén listas..."
sleep 10

# Verificar PostgreSQL
print_message "🔍 Verificando PostgreSQL..."
for i in {1..30}; do
    if docker-compose exec -T postgres pg_isready -U smarthydro -d smarthydro_business &> /dev/null; then
        print_success "✅ PostgreSQL está listo"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "❌ PostgreSQL no se pudo conectar después de 30 intentos"
        exit 1
    fi
    sleep 2
done

# Verificar MongoDB
print_message "🔍 Verificando MongoDB..."
for i in {1..30}; do
    if docker-compose exec -T mongodb mongosh --eval "db.adminCommand('ping')" &> /dev/null; then
        print_success "✅ MongoDB está listo"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "❌ MongoDB no se pudo conectar después de 30 intentos"
        exit 1
    fi
    sleep 2
done

# Verificar Redis
print_message "🔍 Verificando Redis..."
for i in {1..30}; do
    if docker-compose exec -T redis redis-cli ping &> /dev/null; then
        print_success "✅ Redis está listo"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "❌ Redis no se pudo conectar después de 30 intentos"
        exit 1
    fi
    sleep 2
done

# Iniciar Kafka
print_message "🚀 Iniciando Kafka..."
docker-compose up -d kafka

# Esperar a que Kafka esté listo
print_message "⏳ Esperando a que Kafka esté listo..."
sleep 15

# Verificar Kafka
print_message "🔍 Verificando Kafka..."
for i in {1..30}; do
    if docker-compose exec -T kafka kafka-topics --bootstrap-server localhost:9092 --list &> /dev/null; then
        print_success "✅ Kafka está listo"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "❌ Kafka no se pudo conectar después de 30 intentos"
        exit 1
    fi
    sleep 2
done

# Iniciar microservicios
print_message "🚀 Iniciando microservicios..."
docker-compose up -d telemetry-collector data-processor business-api analytics-engine dga-compliance

# Iniciar monitoring
print_message "🚀 Iniciando servicios de monitoring..."
docker-compose up -d prometheus grafana

# Iniciar nginx
print_message "🚀 Iniciando Nginx..."
docker-compose up -d nginx

# Esperar a que todos los servicios estén listos
print_message "⏳ Esperando a que todos los servicios estén listos..."
sleep 30

# Verificar health checks
print_message "🔍 Verificando health checks..."
docker-compose ps

# Verificar endpoints
print_message "🔍 Verificando endpoints..."

# Función para verificar endpoint
check_endpoint() {
    local service=$1
    local port=$2
    local endpoint=$3
    
    for i in {1..10}; do
        if curl -f "http://localhost:${port}${endpoint}" &> /dev/null; then
            print_success "✅ ${service} está respondiendo"
            return 0
        fi
        sleep 2
    done
    print_warning "⚠️  ${service} no responde (puede estar iniciando)"
    return 1
}

check_endpoint "Telemetry Collector" "8001" "/health"
check_endpoint "Business API" "8004" "/health"
check_endpoint "Data Processor" "8003" "/health"
check_endpoint "Analytics Engine" "8005" "/health"
check_endpoint "DGA Compliance" "8002" "/health"
check_endpoint "Prometheus" "9090" "/-/healthy"
check_endpoint "Grafana" "3000" "/api/health"

# Mostrar información de acceso
echo
print_success "🎉 SmartHydro está listo!"
echo
echo -e "${GREEN}📊 Dashboards y Monitoreo:${NC}"
echo -e "   Grafana:     ${BLUE}http://localhost:3000${NC} (admin/admin)"
echo -e "   Prometheus:  ${BLUE}http://localhost:9090${NC}"
echo
echo -e "${GREEN}🔌 APIs:${NC}"
echo -e "   Business API:        ${BLUE}http://localhost:8004${NC}"
echo -e "   Telemetry Collector: ${BLUE}http://localhost:8001${NC}"
echo -e "   Data Processor:      ${BLUE}http://localhost:8003${NC}"
echo -e "   Analytics Engine:    ${BLUE}http://localhost:8005${NC}"
echo -e "   DGA Compliance:      ${BLUE}http://localhost:8002${NC}"
echo
echo -e "${GREEN}🗄️  Bases de Datos:${NC}"
echo -e "   PostgreSQL: ${BLUE}localhost:5432${NC}"
echo -e "   MongoDB:    ${BLUE}localhost:27017${NC}"
echo -e "   Redis:      ${BLUE}localhost:6379${NC}"
echo -e "   Kafka:      ${BLUE}localhost:9092${NC}"
echo
echo -e "${GREEN}📋 Comandos Útiles:${NC}"
echo -e "   Ver logs:           ${BLUE}docker-compose logs -f${NC}"
echo -e "   Ver servicios:      ${BLUE}docker-compose ps${NC}"
echo -e "   Parar servicios:    ${BLUE}./scripts/stop.sh${NC}"
echo -e "   Limpiar todo:       ${BLUE}./scripts/clean.sh${NC}"
echo

# Mostrar logs recientes
print_message "📋 Mostrando logs recientes..."
docker-compose logs --tail=20

print_success "🎯 SmartHydro iniciado exitosamente!"
print_message "💡 Para ver logs en tiempo real: docker-compose logs -f"
print_message "💡 Para parar servicios: ./scripts/stop.sh" 