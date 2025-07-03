#!/usr/bin/env python3
"""
Script para generar migraciones de los modelos base
"""
import os
import sys
import subprocess
from pathlib import Path

# Agregar el directorio del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n🔄 {description}")
    print(f"Comando: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=project_root
        )
        
        if result.stdout:
            print("✅ Salida:")
            print(result.stdout)
        
        if result.stderr:
            print("⚠️  Errores:")
            print(result.stderr)
        
        if result.returncode != 0:
            print(f"❌ Error: Comando falló con código {result.returncode}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error ejecutando comando: {e}")
        return False

def main():
    """Función principal"""
    
    print("🚀 GENERANDO MIGRACIONES PARA MODELOS BASE")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not (project_root / "manage.py").exists():
        print("❌ Error: No se encontró manage.py en el directorio actual")
        return
    
    # 1. Verificar el estado actual
    print("\n📋 Verificando estado actual de las migraciones...")
    run_command("python manage.py showmigrations", "Mostrando migraciones existentes")
    
    # 2. Generar migraciones para la app core
    print("\n🏗️ Generando migraciones para la app core...")
    success = run_command("python manage.py makemigrations core", "Generando migraciones para core")
    
    if not success:
        print("❌ Error generando migraciones para core")
        return
    
    # 3. Generar migraciones para todas las apps
    print("\n🏗️ Generando migraciones para todas las apps...")
    success = run_command("python manage.py makemigrations", "Generando migraciones para todas las apps")
    
    if not success:
        print("❌ Error generando migraciones")
        return
    
    # 4. Mostrar las migraciones generadas
    print("\n📋 Mostrando migraciones generadas...")
    run_command("python manage.py showmigrations", "Mostrando migraciones después de los cambios")
    
    # 5. Verificar sintaxis de los modelos
    print("\n🔍 Verificando sintaxis de los modelos...")
    run_command("python manage.py check", "Verificando configuración de Django")
    
    print("\n✅ Proceso completado!")
    print("\n💡 Próximos pasos:")
    print("   1. Revisar las migraciones generadas")
    print("   2. Ejecutar: python manage.py migrate")
    print("   3. Probar la aplicación")
    print("   4. Verificar que los modelos funcionan correctamente")

if __name__ == "__main__":
    main() 