#!/usr/bin/env python3
"""
Script para generar documentación automática de la API
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

def generate_schema():
    """Generar schema de la API"""
    print("📚 Generando documentación de la API...")
    
    try:
        django.setup()
        from django.core.management import execute_from_command_line
        
        # Generar schema
        print("🔄 Generando schema OpenAPI...")
        execute_from_command_line(['manage.py', 'spectacular', '--file', 'api_schema.json'])
        
        print("✅ Schema generado: api_schema.json")
        
        # Generar documentación HTML
        print("🔄 Generando documentación HTML...")
        execute_from_command_line(['manage.py', 'spectacular', '--file', 'api_docs.html', '--format', 'html'])
        
        print("✅ Documentación HTML generada: api_docs.html")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generando documentación: {e}")
        return False

def show_documentation_info():
    """Mostrar información sobre la documentación"""
    print("\n📖 Información de Documentación")
    print("=" * 50)
    
    print("\n🔗 URLs de Documentación:")
    print("   Swagger UI: http://localhost:8000/api/schema/swagger-ui/")
    print("   ReDoc: http://localhost:8000/api/schema/redoc/")
    print("   Schema JSON: http://localhost:8000/api/schema/")
    
    print("\n📋 Características:")
    print("   ✅ Documentación automática")
    print("   ✅ Ejemplos de uso")
    print("   ✅ Interfaz interactiva")
    print("   ✅ Autenticación integrada")
    print("   ✅ Testing directo desde la UI")
    
    print("\n🎯 Endpoints Documentados:")
    print("   🔧 API Base (Servicio Interno)")
    print("   🎨 API Frontend (Capa Externa)")
    print("   📊 Dashboard y resúmenes")
    print("   👥 Gestión de usuarios")
    print("   📈 Variables y esquemas")

def main():
    """Función principal"""
    print("🚀 Generador de Documentación API")
    print("=" * 50)
    
    # Generar documentación
    if generate_schema():
        print("\n🎉 Documentación generada exitosamente!")
        
        # Mostrar información
        show_documentation_info()
        
        print("\n💡 Para ver la documentación:")
        print("   1. Ejecuta: ./scripts/run-docker-simple.sh")
        print("   2. Abre: http://localhost:8000/api/schema/swagger-ui/")
        
    else:
        print("\n❌ Error generando documentación")
        sys.exit(1)

if __name__ == "__main__":
    main() 