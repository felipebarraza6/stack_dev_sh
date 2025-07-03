#!/bin/bash

# Script de entrada para Docker
set -e

echo "🚀 Iniciando aplicación Django..."

# Crear directorio de logs si no existe
mkdir -p /code/logs
chmod 755 /code/logs

# Ejecutar migraciones
echo "📊 Ejecutando migraciones..."
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Ejecutar el comando pasado como argumento
echo "▶️ Ejecutando comando: $@"
exec "$@" 