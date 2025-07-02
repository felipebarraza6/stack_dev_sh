#!/bin/bash

# Script de verificación rápida del sistema
echo "🔍 Verificación rápida del sistema Stack VPS..."

# Verificar Docker
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está corriendo"
    exit 1
fi
echo "✅ Docker está corriendo"

# Verificar archivos necesarios
required_files=(
    "docker/development/dev.yml"
    "docker/development/conf/nginx-dev.conf"
    "docker/development/conf/mosquitto.conf"
    "api/settings.py"
    "api/celery.py"
    "scripts/run-dev.sh"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file - NO ENCONTRADO"
        exit 1
    fi
done

# Verificar directorios
required_dirs=(
    "api"
    "docker/development"
    "docker/production"
    "scripts"
    "docs"
    "monitoring"
)

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir/"
    else
        echo "❌ $dir/ - NO ENCONTRADO"
        exit 1
    fi
done

echo ""
echo "✅ Verificación rápida completada"
echo "Para verificación completa: python scripts/verificar_sistema_completo.py" 