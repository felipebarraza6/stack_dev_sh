#!/bin/bash

# SmartHydro Microservices - Script de Limpieza
# Este script limpia completamente SmartHydro (¡CUIDADO!)

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

print_message "🧹 Limpiando SmartHydro Microservices..."

# Verificar si Docker Compose está disponible
if ! command -v docker-compose &> /dev/null; then
    print_error "❌ Docker Compose no está instalado"
    exit 1
fi

# ADVERTENCIA IMPORTANTE
echo -e "${RED}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║                    ⚠️  ADVERTENCIA ⚠️                        ║
╠══════════════════════════════════════════════════════════════╣
║  Este script eliminará TODOS los datos de SmartHydro:       ║
║                                                              ║
║  • Contenedores Docker                                       ║
║  • Volúmenes de datos (PostgreSQL, MongoDB, Redis)          ║
║  • Imágenes Docker                                           ║
║  • Redes Docker                                              ║
║  • Logs y archivos temporales                               ║
║                                                              ║
║  ⚠️  ESTA ACCIÓN NO SE PUEDE DESHACER ⚠️                    ║
╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Confirmación múltiple
echo
read -p "¿Estás SEGURO de que quieres eliminar TODOS los datos? (escribe 'ELIMINAR'): " -r
if [[ $REPLY != "ELIMINAR" ]]; then
    print_message "Operación cancelada"
    exit 0
fi

echo
read -p "¿Estás COMPLETAMENTE seguro? Esto eliminará todos los datos. (escribe 'SI, ELIMINAR'): " -r
if [[ $REPLY != "SI, ELIMINAR" ]]; then
    print_message "Operación cancelada"
    exit 0
fi

print_message "🧹 Iniciando limpieza completa..."

# Detener y eliminar contenedores
print_message "🛑 Deteniendo y eliminando contenedores..."
docker-compose down -v --remove-orphans

# Eliminar imágenes
print_message "🗑️  Eliminando imágenes Docker..."
docker-compose down --rmi all --remove-orphans

# Eliminar volúmenes específicos de SmartHydro
print_message "🗑️  Eliminando volúmenes..."
docker volume ls -q | grep smarthydro | xargs -r docker volume rm

# Eliminar redes específicas de SmartHydro
print_message "🗑️  Eliminando redes..."
docker network ls -q | grep smarthydro | xargs -r docker network rm

# Limpiar recursos no utilizados
print_message "🧹 Limpiando recursos no utilizados..."
docker system prune -a -f --volumes

# Eliminar archivos temporales
print_message "🗑️  Eliminando archivos temporales..."
rm -rf logs/*
rm -rf media/*
rm -rf .pytest_cache
rm -rf __pycache__
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Verificar limpieza
print_message "🔍 Verificando limpieza..."

# Verificar contenedores
if docker ps -a | grep -q smarthydro; then
    print_warning "⚠️  Algunos contenedores de SmartHydro aún existen"
    docker ps -a | grep smarthydro
else
    print_success "✅ Todos los contenedores eliminados"
fi

# Verificar volúmenes
if docker volume ls | grep -q smarthydro; then
    print_warning "⚠️  Algunos volúmenes de SmartHydro aún existen"
    docker volume ls | grep smarthydro
else
    print_success "✅ Todos los volúmenes eliminados"
fi

# Verificar imágenes
if docker images | grep -q smarthydro; then
    print_warning "⚠️  Algunas imágenes de SmartHydro aún existen"
    docker images | grep smarthydro
else
    print_success "✅ Todas las imágenes eliminadas"
fi

# Verificar redes
if docker network ls | grep -q smarthydro; then
    print_warning "⚠️  Algunas redes de SmartHydro aún existen"
    docker network ls | grep smarthydro
else
    print_success "✅ Todas las redes eliminadas"
fi

# Mostrar espacio liberado
print_message "💾 Espacio liberado:"
docker system df

print_success "🎯 Limpieza completada exitosamente!"
print_message "💡 Para reiniciar desde cero: ./scripts/start.sh"
print_message "💡 Recuerda configurar el archivo .env antes de reiniciar" 