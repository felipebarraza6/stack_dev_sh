#!/usr/bin/env python3
"""
Script de prueba para el sistema de notificaciones de SmartHydro
"""
import os
import sys
import django
import asyncio
import httpx
import json
from datetime import datetime

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from api.apps.notifications.models import NotificationTemplate, NotificationPreference
from api.apps.notifications.services import NotificationService

User = get_user_model()


def test_django_notification_system():
    """Probar el sistema de notificaciones de Django"""
    print("🔍 Probando sistema de notificaciones Django...")
    
    try:
        # Verificar que existen plantillas
        templates = NotificationTemplate.objects.filter(is_active=True)
        print(f"✅ Plantillas encontradas: {templates.count()}")
        
        # Verificar que existe al menos un usuario
        users = User.objects.all()
        if users.exists():
            user = users.first()
            print(f"✅ Usuario encontrado: {user.email}")
            
            # Crear preferencias de notificación
            preference, created = NotificationPreference.objects.get_or_create(
                user=user,
                module='global',
                defaults={
                    'email_enabled': True,
                    'websocket_enabled': True
                }
            )
            print(f"✅ Preferencias creadas/actualizadas para {user.email}")
            
            # Probar servicio de notificaciones
            service = NotificationService()
            
            # Enviar notificación de prueba
            notifications = service.send_notification(
                template_name='system_test',
                module='global',
                users=[user],
                context_data={
                    'test_message': 'Prueba del sistema de notificaciones',
                    'timestamp': datetime.now().isoformat()
                },
                priority='medium'
            )
            
            print(f"✅ Notificación enviada: {len(notifications)} notificaciones creadas")
            
        else:
            print("⚠️  No se encontraron usuarios para probar")
            
    except Exception as e:
        print(f"❌ Error en sistema Django: {e}")
        return False
    
    return True


async def test_fastapi_notification_service():
    """Probar el microservicio de notificaciones FastAPI"""
    print("\n🔍 Probando microservicio de notificaciones FastAPI...")
    
    try:
        # URL del servicio
        service_url = "http://localhost:8006"
        
        async with httpx.AsyncClient() as client:
            # Health check
            response = await client.get(f"{service_url}/health")
            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ Health check exitoso: {health_data['status']}")
                print(f"   Conexiones: {health_data['connections']}")
            else:
                print(f"❌ Health check falló: {response.status_code}")
                return False
            
            # Obtener módulos disponibles
            response = await client.get(f"{service_url}/modules")
            if response.status_code == 200:
                modules = response.json()
                print(f"✅ Módulos disponibles: {len(modules)} módulos")
            else:
                print(f"❌ Error obteniendo módulos: {response.status_code}")
            
            # Obtener plantillas
            response = await client.get(f"{service_url}/templates")
            if response.status_code == 200:
                templates = response.json()
                print(f"✅ Plantillas disponibles: {len(templates)} plantillas")
            else:
                print(f"❌ Error obteniendo plantillas: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Error en microservicio FastAPI: {e}")
        return False
    
    return True


def test_database_connections():
    """Probar conexiones a base de datos"""
    print("\n🔍 Probando conexiones a base de datos...")
    
    try:
        # Probar conexión a PostgreSQL
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Conexión a PostgreSQL exitosa")
        
        # Probar conexión a Redis
        import redis
        r = redis.Redis(
            host=os.environ.get('REDIS_HOST', 'localhost'),
            port=int(os.environ.get('REDIS_PORT', 6379)),
            password=os.environ.get('REDIS_PASSWORD', 'smarthydro123'),
            decode_responses=True
        )
        r.ping()
        print("✅ Conexión a Redis exitosa")
        
    except Exception as e:
        print(f"❌ Error en conexiones: {e}")
        return False
    
    return True


def create_test_templates():
    """Crear plantillas de prueba si no existen"""
    print("\n🔍 Verificando plantillas de prueba...")
    
    try:
        # Plantilla de prueba del sistema
        template, created = NotificationTemplate.objects.get_or_create(
            name='system_test',
            module='global',
            defaults={
                'notification_type': 'both',
                'subject': 'Prueba del sistema - {{ test_message }}',
                'message_template': '''
                Este es un mensaje de prueba del sistema de notificaciones.

                Detalles:
                - Mensaje: {{ test_message }}
                - Timestamp: {{ timestamp }}
                - Usuario: {{ user.email }}

                Sistema funcionando correctamente.
                ''',
                'available_variables': {
                    'test_message': 'Mensaje de prueba',
                    'timestamp': 'Timestamp del evento',
                    'user': 'Usuario destinatario'
                }
            }
        )
        
        if created:
            print("✅ Plantilla de prueba creada")
        else:
            print("✅ Plantilla de prueba ya existe")
            
    except Exception as e:
        print(f"❌ Error creando plantillas: {e}")


def main():
    """Función principal"""
    print("🚀 Iniciando pruebas del sistema de notificaciones SmartHydro")
    print("=" * 60)
    
    # Crear plantillas de prueba
    create_test_templates()
    
    # Probar conexiones
    db_ok = test_database_connections()
    
    if db_ok:
        # Probar sistema Django
        django_ok = test_django_notification_system()
        
        # Probar microservicio FastAPI
        fastapi_ok = asyncio.run(test_fastapi_notification_service())
        
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE PRUEBAS")
        print("=" * 60)
        print(f"Base de datos: {'✅ OK' if db_ok else '❌ ERROR'}")
        print(f"Sistema Django: {'✅ OK' if django_ok else '❌ ERROR'}")
        print(f"Microservicio FastAPI: {'✅ OK' if fastapi_ok else '❌ ERROR'}")
        
        if all([db_ok, django_ok, fastapi_ok]):
            print("\n🎉 ¡Sistema de notificaciones funcionando correctamente!")
        else:
            print("\n⚠️  Algunas pruebas fallaron. Revisar configuración.")
    else:
        print("\n❌ No se pueden ejecutar las pruebas sin conexión a base de datos")


if __name__ == "__main__":
    main() 