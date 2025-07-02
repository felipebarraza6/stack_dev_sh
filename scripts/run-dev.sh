#!/bin/bash

# Script para levantar el sistema en desarrollo
echo "🚀 Iniciando Stack VPS en modo desarrollo..."

# Verificar que Docker esté corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está corriendo. Por favor inicia Docker primero."
    exit 1
fi

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p media files_catchment
mkdir -p static
mkdir -p logs

# Construir y levantar servicios
echo "🔨 Construyendo y levantando servicios..."
docker-compose -f docker/development/dev.yml up --build -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 30

# Verificar estado de los servicios
echo "🔍 Verificando estado de los servicios..."
docker-compose -f docker/development/dev.yml ps

# Mostrar logs de la API
echo "📋 Mostrando logs de la API..."
docker-compose -f docker/development/dev.yml logs api

echo ""
echo "✅ Sistema iniciado correctamente!"
echo ""
echo "🌐 URLs disponibles:"
echo "   - API Django: http://localhost:8000"
echo "   - Nginx: http://localhost:80"
echo "   - Flower (Celery): http://localhost:5555"
echo "   - Redis: localhost:6379"
echo "   - MQTT: localhost:1883"
echo ""
echo "📊 Para ver logs en tiempo real:"
echo "   docker-compose -f docker/development/dev.yml logs -f"
echo ""
echo "🛑 Para detener el sistema:"
echo "   docker-compose -f docker/development/dev.yml down" 