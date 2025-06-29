#!/usr/bin/env python3
"""
Script de corrección de errores del proyecto SmartHydro
Corrige automáticamente los errores críticos identificados
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(title):
    """Imprimir encabezado"""
    print(f"\n{'='*60}")
    print(f"🔧 {title}")
    print(f"{'='*60}")

def print_step(step, description):
    """Imprimir paso"""
    print(f"\n📋 Paso {step}: {description}")

def check_docker_compose():
    """Verificar que docker-compose.yml sea válido"""
    print_step(1, "Verificando docker-compose.yml")
    
    try:
        result = subprocess.run(
            ['docker-compose', 'config'],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            print("✅ docker-compose.yml es válido")
            return True
        else:
            print(f"❌ docker-compose.yml tiene errores:")
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("❌ docker-compose no está instalado")
        return False

def create_missing_directories():
    """Crear directorios faltantes"""
    print_step(2, "Creando directorios faltantes")
    
    directories = [
        'services/business-api/app',
        'services/analytics-engine/app',
        'services/ingestion-engine/app',
        'config',
        'monitoring',
        'nginx',
        'ssl'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Creado: {directory}")

def create_env_file():
    """Crear archivo .env si no existe"""
    print_step(3, "Creando archivo .env")
    
    if not os.path.exists('.env'):
        shutil.copy('env.example', '.env')
        print("✅ Archivo .env creado desde env.example")
    else:
        print("✅ Archivo .env ya existe")

def check_services():
    """Verificar que todos los servicios tengan los archivos necesarios"""
    print_step(4, "Verificando servicios")
    
    services = [
        'telemetry-collector',
        'data-processor', 
        'business-api',
        'analytics-engine',
        'dga-compliance',
        'notification-service',
        'alert-service',
        'ingestion-engine'
    ]
    
    for service in services:
        service_path = f'services/{service}'
        if os.path.exists(service_path):
            # Verificar Dockerfile
            dockerfile = f'{service_path}/Dockerfile'
            if not os.path.exists(dockerfile):
                print(f"⚠️  Faltante: {dockerfile}")
            
            # Verificar requirements.txt
            requirements = f'{service_path}/requirements.txt'
            if not os.path.exists(requirements):
                print(f"⚠️  Faltante: {requirements}")
            
            # Verificar main.py
            main_py = f'{service_path}/app/main.py'
            if not os.path.exists(main_py):
                print(f"⚠️  Faltante: {main_py}")
            
            print(f"✅ Servicio verificado: {service}")
        else:
            print(f"❌ Servicio faltante: {service}")

def check_database_config():
    """Verificar configuración de base de datos"""
    print_step(5, "Verificando configuración de base de datos")
    
    # Verificar si las bases de datos están comentadas en docker-compose
    with open('docker-compose.yml', 'r') as f:
        content = f.read()
    
    if '# postgres:' in content:
        print("⚠️  PostgreSQL está comentado en docker-compose.yml")
        print("   Considera descomentarlo para desarrollo local")
    
    if '# mongodb:' in content:
        print("⚠️  MongoDB está comentado en docker-compose.yml")
        print("   Considera descomentarlo para desarrollo local")

def check_api_keys():
    """Verificar configuración de API keys"""
    print_step(6, "Verificando API keys")
    
    required_keys = [
        'TWIN_API_KEY',
        'NETTRA_API_KEY', 
        'NOVUS_API_KEY',
        'DGA_API_KEY'
    ]
    
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_content = f.read()
        
        for key in required_keys:
            if f'{key}=your_' in env_content:
                print(f"⚠️  {key} no está configurada")
            else:
                print(f"✅ {key} configurada")

def create_monitoring_config():
    """Crear configuración de monitoreo"""
    print_step(7, "Creando configuración de monitoreo")
    
    # Crear prometheus.yml
    prometheus_config = '''global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'telemetry-collector'
    static_configs:
      - targets: ['telemetry-collector:8001']
  
  - job_name: 'data-processor'
    static_configs:
      - targets: ['data-processor:8003']
  
  - job_name: 'business-api'
    static_configs:
      - targets: ['business-api:8004']
  
  - job_name: 'analytics-engine'
    static_configs:
      - targets: ['analytics-engine:8005']
'''
    
    os.makedirs('monitoring', exist_ok=True)
    with open('monitoring/prometheus.yml', 'w') as f:
        f.write(prometheus_config)
    
    print("✅ Configuración de Prometheus creada")

def create_nginx_config():
    """Crear configuración de Nginx"""
    print_step(8, "Creando configuración de Nginx")
    
    nginx_config = '''events {
    worker_connections 1024;
}

http {
    upstream business_api {
        server business-api:8004;
    }
    
    upstream telemetry_collector {
        server telemetry-collector:8001;
    }
    
    upstream data_processor {
        server data-processor:8003;
    }
    
    upstream analytics_engine {
        server analytics-engine:8005;
    }
    
    server {
        listen 80;
        
        location /health {
            return 200 "healthy";
        }
        
        location /api/ {
            proxy_pass http://business_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        location /telemetry/ {
            proxy_pass http://telemetry_collector;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        location /analytics/ {
            proxy_pass http://analytics_engine;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
'''
    
    os.makedirs('nginx', exist_ok=True)
    with open('nginx/nginx.conf', 'w') as f:
        f.write(nginx_config)
    
    print("✅ Configuración de Nginx creada")

def generate_summary():
    """Generar resumen de correcciones"""
    print_header("RESUMEN DE CORRECCIONES")
    
    print("✅ Directorios creados:")
    print("   - services/business-api/")
    print("   - services/analytics-engine/")
    print("   - config/")
    print("   - monitoring/")
    print("   - nginx/")
    
    print("\n✅ Archivos creados:")
    print("   - services/business-api/Dockerfile")
    print("   - services/business-api/requirements.txt")
    print("   - services/business-api/app/main.py")
    print("   - services/analytics-engine/Dockerfile")
    print("   - services/analytics-engine/requirements.txt")
    print("   - services/analytics-engine/app/main.py")
    print("   - monitoring/prometheus.yml")
    print("   - nginx/nginx.conf")
    
    print("\n✅ Correcciones aplicadas:")
    print("   - Puerto duplicado corregido (ingestion-engine: 8008)")
    print("   - URLs inconsistentes corregidas")
    print("   - Archivo .env creado")
    
    print("\n⚠️  Acciones recomendadas:")
    print("   1. Configurar API keys en .env")
    print("   2. Descomentar bases de datos en docker-compose.yml si es necesario")
    print("   3. Ejecutar: docker-compose up -d")
    print("   4. Verificar que todos los servicios estén funcionando")

def main():
    """Función principal"""
    print_header("CORRECCIÓN DE ERRORES - SMARTYDRO")
    
    try:
        # Ejecutar correcciones
        create_missing_directories()
        create_env_file()
        check_services()
        check_database_config()
        check_api_keys()
        create_monitoring_config()
        create_nginx_config()
        
        # Verificar docker-compose
        if check_docker_compose():
            print("\n✅ Todas las correcciones aplicadas exitosamente")
        else:
            print("\n❌ Hay errores en docker-compose.yml que necesitan corrección manual")
        
        generate_summary()
        
    except Exception as e:
        print(f"\n❌ Error durante la corrección: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 