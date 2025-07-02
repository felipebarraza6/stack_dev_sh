#!/usr/bin/env python3
"""
Script de Verificación Completa del Sistema
Valida la correcta instalación y funcionamiento de todas las apps modulares
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / 'api'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Error configurando Django: {e}")
    sys.exit(1)

from django.apps import apps
from django.db import connection
from django.core.management import execute_from_command_line
from django.conf import settings


def verificar_apps_instaladas():
    """Verifica que todas las apps estén correctamente instaladas"""
    print("🔍 Verificando apps instaladas...")
    
    apps_requeridas = [
    
        'users', 
        'providers',
        'variables',
        'catchment',
        'compliance',
        'telemetry'
    ]
    
    apps_instaladas = [app.name.split('.')[-1] for app in apps.get_app_configs()]
    
    for app in apps_requeridas:
        if app in apps_instaladas:
            print(f"   ✅ {app}")
        else:
            print(f"   ❌ {app} - NO INSTALADA")
            return False
    
    return True


def verificar_modelos():
    """Verifica que los modelos estén correctamente definidos"""
    print("\n🔍 Verificando modelos...")
    
    modelos_requeridos = {
    
        'users': ['User', 'UserProfile', 'UserRole', 'UserRoleAssignment', 'CatchmentPointOwner', 'CatchmentPointNotification'],
        'providers': ['Provider', 'ProviderConfig', 'ProviderToken'],
        'variables': ['Variable', 'VariableConfig', 'VariableRule'],
        'catchment': ['CatchmentPoint', 'CatchmentPointConfig'],
        'compliance': ['ComplianceSource', 'ComplianceConfig', 'ComplianceData', 'ComplianceRule', 'ComplianceNotification', 'ComplianceLog'],
        'telemetry': ['TelemetryData', 'TelemetryConfig']
    }
    
    for app, modelos in modelos_requeridos.items():
        try:
            app_config = apps.get_app_config(app)
            for modelo in modelos:
                try:
                    model = app_config.get_model(modelo)
                    print(f"   ✅ {app}.{modelo}")
                except LookupError:
                    print(f"   ❌ {app}.{modelo} - NO ENCONTRADO")
                    return False
        except LookupError:
            print(f"   ❌ App {app} - NO ENCONTRADA")
            return False
    
    return True


def verificar_base_datos():
    """Verifica la conectividad y estructura de la base de datos"""
    print("\n🔍 Verificando base de datos...")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"   ✅ Conexión exitosa - {version[0]}")
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return False
    
    # Verificar tablas
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tablas = [row[0] for row in cursor.fetchall()]
            
            tablas_esperadas = [
        
                'users_user', 'users_userprofile', 'users_userrole',
                'providers_provider', 'providers_providerconfig',
                'variables_variable', 'variables_variableconfig',
                'catchment_catchmentpoint', 'catchment_catchmentpointconfig',
                'compliance_compliance_source', 'compliance_compliance_config',
                'telemetry_telemetrydata'
            ]
            
            for tabla in tablas_esperadas:
                if tabla in tablas:
                    print(f"   ✅ Tabla {tabla}")
                else:
                    print(f"   ⚠️  Tabla {tabla} - NO ENCONTRADA (puede necesitar migración)")
    
    except Exception as e:
        print(f"   ❌ Error verificando tablas: {e}")
        return False
    
    return True


def verificar_configuracion():
    """Verifica la configuración del sistema"""
    print("\n🔍 Verificando configuración...")
    
    configuraciones = [
        ('DEBUG', settings.DEBUG),
        ('SECRET_KEY', bool(settings.SECRET_KEY)),
        ('DATABASES', bool(settings.DATABASES)),
        ('REDIS_URL', hasattr(settings, 'REDIS_URL')),
        ('MQTT_BROKER', hasattr(settings, 'MQTT_BROKER')),
        ('CELERY_BROKER_URL', hasattr(settings, 'CELERY_BROKER_URL')),
    ]
    
    for config, valor in configuraciones:
        if valor:
            print(f"   ✅ {config}")
        else:
            print(f"   ❌ {config} - NO CONFIGURADO")
            return False
    
    return True


def verificar_archivos():
    """Verifica que los archivos necesarios existan"""
    print("\n🔍 Verificando archivos...")
    
    archivos_requeridos = [
        'api/settings.py',
        'api/urls.py',
        'api/celery.py',
        'dev.yml',
        'conf/nginx-dev.conf',
        'conf/mosquitto.conf',
        'run-dev.sh'
    ]
    
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} - NO ENCONTRADO")
            return False
    
    return True


def verificar_dependencias():
    """Verifica las dependencias de Python"""
    print("\n🔍 Verificando dependencias...")
    
    dependencias = [
        'django',
        'djangorestframework',
        'celery',
        'redis',
        'paho-mqtt',
        'pandas',
        'numpy'
    ]
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"   ✅ {dep}")
        except ImportError:
            print(f"   ❌ {dep} - NO INSTALADA")
            return False
    
    return True


def verificar_celery():
    """Verifica la configuración de Celery"""
    print("\n🔍 Verificando Celery...")
    
    try:
        from api.celery import app
        print("   ✅ Configuración de Celery cargada")
        
        # Verificar tareas registradas
        tareas = list(app.tasks.keys())
        tareas_esperadas = [
            'tasks.telemetry.process_telemetry_data',
            'tasks.telemetry.send_compliance_data',
            'tasks.telemetry.health_check'
        ]
        
        for tarea in tareas_esperadas:
            if tarea in tareas:
                print(f"   ✅ Tarea {tarea}")
            else:
                print(f"   ⚠️  Tarea {tarea} - NO REGISTRADA")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en Celery: {e}")
        return False


def ejecutar_migraciones():
    """Ejecuta las migraciones pendientes"""
    print("\n🔧 Ejecutando migraciones...")
    
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("   ✅ Migraciones completadas")
        return True
    except Exception as e:
        print(f"   ❌ Error en migraciones: {e}")
        return False


def crear_superusuario():
    """Crea un superusuario si no existe"""
    print("\n👤 Verificando superusuario...")
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if User.objects.filter(is_superuser=True).exists():
            print("   ✅ Superusuario ya existe")
            return True
        else:
            print("   ⚠️  No hay superusuario. Creando uno...")
            # Aquí podrías crear un superusuario automáticamente
            return True
            
    except Exception as e:
        print(f"   ❌ Error verificando superusuario: {e}")
        return False


def main():
    """Función principal de verificación"""
    print("🚀 VERIFICACIÓN COMPLETA DEL SISTEMA STACK VPS")
    print("=" * 50)
    
    verificaciones = [
        ("Apps instaladas", verificar_apps_instaladas),
        ("Modelos", verificar_modelos),
        ("Base de datos", verificar_base_datos),
        ("Configuración", verificar_configuracion),
        ("Archivos", verificar_archivos),
        ("Dependencias", verificar_dependencias),
        ("Celery", verificar_celery),
    ]
    
    resultados = []
    
    for nombre, funcion in verificaciones:
        try:
            resultado = funcion()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"   ❌ Error en {nombre}: {e}")
            resultados.append((nombre, False))
    
    # Resumen final
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 50)
    
    exitos = sum(1 for _, resultado in resultados if resultado)
    total = len(resultados)
    
    for nombre, resultado in resultados:
        estado = "✅ EXITOSO" if resultado else "❌ FALLIDO"
        print(f"{nombre}: {estado}")
    
    print(f"\nTotal: {exitos}/{total} verificaciones exitosas")
    
    if exitos == total:
        print("\n🎉 ¡SISTEMA VERIFICADO CORRECTAMENTE!")
        print("\nPara iniciar el sistema en desarrollo:")
        print("   ./run-dev.sh")
        print("\nPara verificar el estado:")
        print("   docker-compose -f dev.yml ps")
        return 0
    else:
        print(f"\n⚠️  {total - exitos} verificaciones fallaron")
        print("Revisa los errores anteriores y corrige los problemas")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 