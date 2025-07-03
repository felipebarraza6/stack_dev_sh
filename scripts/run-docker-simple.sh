#!/bin/bash

# Script para ejecutar configuración Docker simplificada
# Solo modelo base, SQLite, sin telemetría

echo "🐳 Configuración Docker Simplificada"
echo "=================================================="
echo "📊 Base de datos: SQLite"
echo "🔧 Apps: Core, Users, Frontend"
echo "📡 Telemetría: Deshabilitada"
echo "🧪 Modo: Testing de endpoints"
echo "=================================================="

# Verificar que Docker esté corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está corriendo. Por favor inicia Docker Desktop."
    exit 1
fi

# Verificar que docker-compose esté disponible
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose no está instalado."
    exit 1
fi

# Navegar al directorio del proyecto
cd "$(dirname "$0")/.."

# Detener contenedores existentes si los hay
echo "🛑 Deteniendo contenedores existentes..."
docker-compose -f docker/development/dev-simple.yml down

# Construir y ejecutar
echo "🔨 Construyendo y ejecutando contenedores..."
docker-compose -f docker/development/dev-simple.yml up --build

echo ""
echo "📋 Endpoints Disponibles:"
echo "=================================================="
echo ""
echo "🔧 API Base (Servicio Interno):"
echo "   http://localhost:8000/api/base/"
echo "   - Variables básicas"
echo "   - Esquemas básicos"
echo "   - Usuarios básicos"
echo ""
echo "🎨 API Frontend (Capa Externa):"
echo "   http://localhost:8000/api/frontend/"
echo "   - Variables con campos adicionales"
echo "   - Dashboard con caché"
echo "   - Funcionalidades frontend"
echo ""
echo "🔐 Admin Django:"
echo "   http://localhost:8000/admin/"
echo "   - Usuario: admin"
echo "   - Contraseña: admin123"
echo ""
echo "📚 API Browser:"
echo "   http://localhost:8000/api/frontend/variables/"
echo "   http://localhost:8000/api/base/variables/"
echo ""
echo "📖 Documentación Automática:"
echo "   Swagger UI: http://localhost:8000/api/schema/swagger-ui/"
echo "   ReDoc: http://localhost:8000/api/schema/redoc/"
echo "   Schema JSON: http://localhost:8000/api/schema/"
echo ""
echo "🛑 Para detener: docker-compose -f docker/development/dev-simple.yml down" 