#!/usr/bin/env python3
"""
Script para ejecutar servidor de desarrollo local
Solo modelo base, SQLite, sin telemetría
"""
import os
import sys
import django
from pathlib import Path

# Configurar el path del proyecto
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configurar Django con configuración local
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.config.settings.local')

def setup_database():
    """Configurar base de datos SQLite"""
    print("🗄️ Configurando base de datos SQLite...")
    
    try:
        django.setup()
        from django.core.management import execute_from_command_line
        
        # Crear migraciones
        print("📝 Creando migraciones...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        
        # Aplicar migraciones
        print("🔄 Aplicando migraciones...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Crear superusuario si no existe
        print("👤 Verificando superusuario...")
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            print("👤 Creando superusuario 'admin'...")
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("✅ Superusuario creado: admin/admin123")
        else:
            print("✅ Superusuario ya existe")
            
    except Exception as e:
        print(f"❌ Error configurando base de datos: {e}")
        return False
    
    return True

def run_server():
    """Ejecutar servidor de desarrollo"""
    print("🚀 Iniciando servidor de desarrollo...")
    
    try:
        from django.core.management import execute_from_command_line
        
        # Ejecutar servidor
        execute_from_command_line([
            'manage.py', 'runserver', '0.0.0.0:8000'
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error ejecutando servidor: {e}")

def show_endpoints():
    """Mostrar endpoints disponibles"""
    print("\n📋 Endpoints Disponibles:")
    print("=" * 50)
    
    print("\n🔧 API Base (Servicio Interno):")
    print("   http://localhost:8000/api/base/")
    print("   - Variables básicas")
    print("   - Esquemas básicos")
    print("   - Usuarios básicos")
    
    print("\n🎨 API Frontend (Capa Externa):")
    print("   http://localhost:8000/api/frontend/")
    print("   - Variables con campos adicionales")
    print("   - Dashboard con caché")
    print("   - Funcionalidades frontend")
    
    print("\n🔐 Admin Django:")
    print("   http://localhost:8000/admin/")
    print("   - Usuario: admin")
    print("   - Contraseña: admin123")
    
    print("\n📚 API Browser:")
    print("   http://localhost:8000/api/frontend/variables/")
    print("   http://localhost:8000/api/base/variables/")

def main():
    """Función principal"""
    print("🧪 Configuración de Desarrollo Local")
    print("=" * 50)
    print("📊 Base de datos: SQLite")
    print("🔧 Apps: Core, Users, Frontend")
    print("📡 Telemetría: Deshabilitada")
    print("🧪 Modo: Testing de endpoints")
    print("=" * 50)
    
    # Configurar base de datos
    if not setup_database():
        print("❌ Error en configuración. Saliendo...")
        sys.exit(1)
    
    # Mostrar endpoints
    show_endpoints()
    
    print("\n🚀 Iniciando servidor...")
    print("📱 Presiona Ctrl+C para detener")
    print("=" * 50)
    
    # Ejecutar servidor
    run_server()

if __name__ == "__main__":
    main() 