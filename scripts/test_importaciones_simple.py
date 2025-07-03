#!/usr/bin/env python3
"""
Test Simple de Importaciones - Verifica que las apps se pueden importar
"""

import os
import sys
import importlib
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.config.settings.local')

def test_basic_imports():
    """Test básico de importaciones"""
    
    print("🔍 Test básico de importaciones")
    print("=" * 50)
    
    # Apps principales
    apps = [
        'api.apps.core',
        'api.apps.users', 
        'api.apps.variables',
        'api.apps.catchment',
        'api.apps.compliance',
        'api.apps.telemetry',
        'api.apps.providers',
        'api.apps.frontend',
    ]
    
    success_count = 0
    total_count = len(apps)
    
    for app_name in apps:
        try:
            module = importlib.import_module(app_name)
            print(f"✅ {app_name}")
            success_count += 1
        except Exception as e:
            print(f"❌ {app_name}: {str(e)}")
    
    print(f"\n📊 Resultado: {success_count}/{total_count} apps importadas correctamente")
    
    if success_count == total_count:
        print("🎉 ¡Todas las apps se importan correctamente!")
    else:
        print("⚠️  Hay problemas de importación que necesitan ser corregidos.")

def test_provider_schema_mapping():
    """Test específico del modelo ProviderSchemaMapping"""
    
    print("\n🔧 Test específico: ProviderSchemaMapping")
    print("=" * 50)
    
    try:
        from api.apps.providers.models.providers.provider import ProviderSchemaMapping
        print("✅ ProviderSchemaMapping importado correctamente")
        
        # Verificar que es una clase de modelo
        from django.db import models
        if issubclass(ProviderSchemaMapping, models.Model):
            print("✅ ProviderSchemaMapping es un modelo Django válido")
        else:
            print("❌ ProviderSchemaMapping NO es un modelo Django")
            
    except Exception as e:
        print(f"❌ Error importando ProviderSchemaMapping: {str(e)}")

def test_provider_models():
    """Test de todos los modelos de providers"""
    
    print("\n🏗️  Test de modelos de providers")
    print("=" * 50)
    
    models_to_test = [
        ('api.apps.providers.models.providers.provider', 'Provider'),
        ('api.apps.providers.models.providers.provider', 'ProviderSchemaMapping'),
        ('api.apps.providers.models.mqtt.broker', 'MQTTBroker'),
        ('api.apps.providers.models.tokens.device_token', 'DeviceToken'),
        ('api.apps.providers.models.schemas.data_schema', 'DataSchema'),
        ('api.apps.providers.models.logs.ingestion_log', 'DataIngestionLog'),
    ]
    
    success_count = 0
    total_count = len(models_to_test)
    
    for module_path, model_name in models_to_test:
        try:
            module = importlib.import_module(module_path)
            model_class = getattr(module, model_name)
            print(f"✅ {model_name}")
            success_count += 1
        except Exception as e:
            print(f"❌ {model_name}: {str(e)}")
    
    print(f"\n📊 Resultado: {success_count}/{total_count} modelos importados correctamente")

def test_django_setup():
    """Test de configuración de Django"""
    
    print("\n⚙️  Test de configuración de Django")
    print("=" * 50)
    
    try:
        import django
        django.setup()
        print("✅ Django configurado correctamente")
        
        # Verificar apps registradas
        from django.apps import apps
        registered_apps = [app.name for app in apps.get_app_configs()]
        
        expected_apps = [
            'api.apps.core',
            'api.apps.users',
            'api.apps.variables', 
            'api.apps.catchment',
            'api.apps.compliance',
            'api.apps.telemetry',
            'api.apps.providers',
            'api.apps.frontend',
        ]
        
        missing_apps = []
        for app_name in expected_apps:
            if app_name in registered_apps:
                print(f"✅ {app_name} registrada")
            else:
                print(f"❌ {app_name} NO registrada")
                missing_apps.append(app_name)
        
        if not missing_apps:
            print("🎉 Todas las apps están registradas correctamente")
        else:
            print(f"⚠️  Apps faltantes: {missing_apps}")
            
    except Exception as e:
        print(f"❌ Error configurando Django: {str(e)}")

def main():
    """Función principal"""
    
    print("🚀 Test Simple de Importaciones")
    print("=" * 50)
    
    test_basic_imports()
    test_provider_schema_mapping()
    test_provider_models()
    test_django_setup()
    
    print("\n✨ Test completado")

if __name__ == '__main__':
    main() 