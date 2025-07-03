#!/bin/bash

# Script para ejecutar servidor de desarrollo local
# Solo modelo base, SQLite, sin telemetría

echo "🧪 Configuración de Desarrollo Local"
echo "=================================================="
echo "📊 Base de datos: SQLite"
echo "🔧 Apps: Core, Users, Frontend"
echo "📡 Telemetría: Deshabilitada"
echo "🧪 Modo: Testing de endpoints"
echo "=================================================="

# Configurar variables de entorno
export DJANGO_SETTINGS_MODULE=api.config.settings.local
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Crear directorio de logs si no existe
mkdir -p logs

# Crear migraciones
echo "📝 Creando migraciones..."
python manage.py makemigrations

# Aplicar migraciones
echo "🔄 Aplicando migraciones..."
python manage.py migrate

# Crear superusuario si no existe
echo "👤 Verificando superusuario..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superusuario creado: admin/admin123')
else:
    print('✅ Superusuario ya existe')
"

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
echo "🚀 Iniciando servidor..."
echo "📱 Presiona Ctrl+C para detener"
echo "=================================================="

# Ejecutar servidor
python manage.py runserver 0.0.0.0:8000 