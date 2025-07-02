#!/bin/bash

# Script de limpieza del sistema
echo "🧹 Limpiando sistema Stack VPS..."

# Detener y eliminar contenedores
echo "🛑 Deteniendo contenedores..."
docker-compose -f docker/development/dev.yml down -v

# Eliminar imágenes no utilizadas
echo "🗑️ Eliminando imágenes no utilizadas..."
docker image prune -f

# Eliminar volúmenes no utilizados
echo "🗑️ Eliminando volúmenes no utilizados..."
docker volume prune -f

# Eliminar redes no utilizadas
echo "🗑️ Eliminando redes no utilizadas..."
docker network prune -f

# Limpiar archivos temporales
echo "🧹 Limpiando archivos temporales..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.log" -delete

# Limpiar directorios de desarrollo
echo "🧹 Limpiando directorios de desarrollo..."
rm -rf media/*
rm -rf static/*
rm -f api/db.sqlite3

echo "✅ Limpieza completada!" 