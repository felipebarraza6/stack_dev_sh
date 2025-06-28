#!/bin/bash

# SmartHydro Microservices - Script de Parada
# Este script detiene todos los servicios de SmartHydro

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

print_message "🛑 Deteniendo SmartHydro Microservices..."

# Verificar si Docker Compose está disponible
if ! command -v docker-compose &> /dev/null; then
    print_error "❌ Docker Compose no está instalado"
    exit 1
fi

# Verificar si hay servicios corriendo
if ! docker-compose ps | grep -q "Up"; then
    print_warning "⚠️  No hay servicios corriendo"
    exit 0
fi

# Mostrar servicios activos
print_message "📋 Servicios activos:"
docker-compose ps

# Preguntar confirmación
echo
read -p "¿Estás seguro de que quieres detener todos los servicios? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_message "Operación cancelada"
    exit 0
fi

# Detener servicios
print_message "🛑 Deteniendo servicios..."
docker-compose down

# Verificar que todos los servicios se detuvieron
if docker-compose ps | grep -q "Up"; then
    print_warning "⚠️  Algunos servicios aún están corriendo"
    docker-compose ps
else
    print_success "✅ Todos los servicios han sido detenidos"
fi

# Mostrar estado final
print_message "📋 Estado final:"
docker-compose ps

print_success "🎯 SmartHydro detenido exitosamente!"
print_message "💡 Para reiniciar: ./scripts/start.sh" 