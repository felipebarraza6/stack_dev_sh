#!/usr/bin/env python3
"""
Test de Importaciones - Verifica que todas las apps se pueden importar correctamente
"""

import os
import sys
import importlib
import traceback
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.config.settings.local')

def test_app_imports():
    """Test de importaciones de todas las apps"""
    
    apps_to_test = [
        'api.apps.core',
        'api.apps.users',
        'api.apps.variables',
        'api.apps.catchment',
        'api.apps.compliance',
        'api.apps.telemetry',
        'api.apps.providers',
        'api.apps.frontend',
    ]
    
    print("🔍 Iniciando test de importaciones...")
    print("=" * 60)
    
    results = {}
    
    for app_name in apps_to_test:
        print(f"\n📦 Probando app: {app_name}")
        try:
            # Importar la app
            app_module = importlib.import_module(app_name)
            print(f"   ✅ App importada correctamente")
            
            # Verificar si tiene __all__ definido
            if hasattr(app_module, '__all__'):
                print(f"   📋 __all__ definido: {app_module.__all__}")
                
                # Probar importaciones de __all__
                for item_name in app_module.__all__:
                    try:
                        if hasattr(app_module, '__getattr__'):
                            # Para apps con importación tardía
                            item = getattr(app_module, item_name)
                            print(f"      ✅ {item_name} importado correctamente")
                        else:
                            # Para apps con importación directa
                            item = getattr(app_module, item_name)
                            print(f"      ✅ {item_name} disponible")
                    except Exception as e:
                        print(f"      ❌ Error importando {item_name}: {str(e)}")
            else:
                print(f"   ⚠️  No tiene __all__ definido")
            
            results[app_name] = {'status': 'success', 'error': None}
            
        except Exception as e:
            print(f"   ❌ Error importando app: {str(e)}")
            print(f"   📄 Traceback:")
            traceback.print_exc()
            results[app_name] = {'status': 'error', 'error': str(e)}
    
    return results

def test_model_imports():
    """Test de importaciones de modelos específicos"""
    
    print("\n" + "=" * 60)
    print("🏗️  Test de importaciones de modelos específicos")
    print("=" * 60)
    
    model_imports = [
        # Core
        ('api.apps.core.models.base', 'BaseModel'),
        
        # Users
        ('api.apps.users.models.users.user', 'User'),
        
        # Variables
        ('api.apps.variables.models.variables.variable', 'Variable'),
        ('api.apps.variables.models.schemas.schema', 'VariableSchema'),
        ('api.apps.variables.models.schemas.mapping', 'VariableSchemaMapping'),
        ('api.apps.variables.models.data_points.data_point', 'VariableDataPoint'),
        ('api.apps.variables.models.alerts.alert', 'VariableAlert'),
        ('api.apps.variables.models.alerts.alert_log', 'VariableAlertLog'),
        
        # Catchment
        ('api.apps.catchment.models.points.catchment_point', 'CatchmentPoint'),
        ('api.apps.catchment.models.configs.processing_config', 'CatchmentPointProcessingConfig'),
        ('api.apps.catchment.models.notifications.notification', 'NotificationsCatchment'),
        
        # Compliance
        ('api.apps.compliance.models.sources.compliance_source', 'ComplianceSource'),
        ('api.apps.compliance.models.configs.compliance_config', 'ComplianceConfig'),
        ('api.apps.compliance.models.data.compliance_data', 'ComplianceData'),
        ('api.apps.compliance.models.logs.models', 'ComplianceLog'),
        
        # Telemetry
        ('api.apps.telemetry.models.data.telemetry_data', 'TelemetryData'),
        ('api.apps.telemetry.models.data.raw_telemetry_data', 'RawTelemetryData'),
        ('api.apps.telemetry.models.data.processed_telemetry_data', 'ProcessedTelemetryData'),
        ('api.apps.telemetry.models.schemas.telemetry_schema', 'TelemetrySchema'),
        ('api.apps.telemetry.models.schemas.response_schema', 'ResponseSchema'),
        
        # Providers
        ('api.apps.providers.models.providers.provider', 'Provider'),
        ('api.apps.providers.models.providers.provider', 'ProviderSchemaMapping'),
        ('api.apps.providers.models.mqtt.broker', 'MQTTBroker'),
        ('api.apps.providers.models.tokens.device_token', 'DeviceToken'),
        ('api.apps.providers.models.schemas.data_schema', 'DataSchema'),
        ('api.apps.providers.models.logs.ingestion_log', 'DataIngestionLog'),
    ]
    
    model_results = {}
    
    for module_path, model_name in model_imports:
        print(f"\n🔧 Probando modelo: {module_path}.{model_name}")
        try:
            module = importlib.import_module(module_path)
            model_class = getattr(module, model_name)
            print(f"   ✅ {model_name} importado correctamente")
            model_results[f"{module_path}.{model_name}"] = {'status': 'success', 'error': None}
        except Exception as e:
            print(f"   ❌ Error importando {model_name}: {str(e)}")
            model_results[f"{module_path}.{model_name}"] = {'status': 'error', 'error': str(e)}
    
    return model_results

def test_serializer_imports():
    """Test de importaciones de serializers"""
    
    print("\n" + "=" * 60)
    print("📝 Test de importaciones de serializers")
    print("=" * 60)
    
    serializer_imports = [
        # Users
        ('api.apps.users.serializers.users.user', 'UserSerializer'),
        
        # Variables
        ('api.apps.variables.serializers.variables.variable', 'VariableSerializer'),
        ('api.apps.variables.serializers.data_points.data_point', 'VariableDataPointSerializer'),
        ('api.apps.variables.serializers.alerts.alert', 'VariableAlertSerializer'),
        
        # Catchment
        ('api.apps.catchment.serializers.points.catchment_point', 'CatchmentPointSerializer'),
        ('api.apps.catchment.serializers.configs.processing_config', 'CatchmentPointProcessingConfigSerializer'),
        ('api.apps.catchment.serializers.notifications.notification', 'NotificationsCatchmentSerializer'),
        
        # Compliance
        ('api.apps.compliance.serializers.sources.compliance_source', 'ComplianceSourceSerializer'),
        ('api.apps.compliance.serializers.configs.compliance_config', 'ComplianceConfigSerializer'),
        ('api.apps.compliance.serializers.data.compliance_data', 'ComplianceDataSerializer'),
        ('api.apps.compliance.serializers.logs.serializers', 'ComplianceLogSerializer'),
        
        # Telemetry
        ('api.apps.telemetry.serializers.data.telemetry_data', 'TelemetryDataSerializer'),
        ('api.apps.telemetry.serializers.schemas.response_schema', 'ResponseSchemaSerializer'),
        
        # Providers
        ('api.apps.providers.serializers.providers.provider', 'ProviderSerializer'),
        ('api.apps.providers.serializers.mqtt.broker', 'MQTTBrokerSerializer'),
        ('api.apps.providers.serializers.tokens.device_token', 'DeviceTokenSerializer'),
        ('api.apps.providers.serializers.schemas.data_schema', 'DataSchemaSerializer'),
        ('api.apps.providers.serializers.logs.ingestion_log', 'DataIngestionLogSerializer'),
    ]
    
    serializer_results = {}
    
    for module_path, serializer_name in serializer_imports:
        print(f"\n📝 Probando serializer: {module_path}.{serializer_name}")
        try:
            module = importlib.import_module(module_path)
            serializer_class = getattr(module, serializer_name)
            print(f"   ✅ {serializer_name} importado correctamente")
            serializer_results[f"{module_path}.{serializer_name}"] = {'status': 'success', 'error': None}
        except Exception as e:
            print(f"   ❌ Error importando {serializer_name}: {str(e)}")
            serializer_results[f"{module_path}.{serializer_name}"] = {'status': 'error', 'error': str(e)}
    
    return serializer_results

def test_django_setup():
    """Test de configuración de Django"""
    
    print("\n" + "=" * 60)
    print("⚙️  Test de configuración de Django")
    print("=" * 60)
    
    try:
        import django
        django.setup()
        print("✅ Django configurado correctamente")
        
        # Verificar que las apps están registradas
        from django.apps import apps
        registered_apps = [app.name for app in apps.get_app_configs()]
        print(f"📋 Apps registradas: {len(registered_apps)}")
        
        # Verificar apps específicas
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
        
        for app_name in expected_apps:
            if app_name in registered_apps:
                print(f"   ✅ {app_name} registrada")
            else:
                print(f"   ❌ {app_name} NO registrada")
        
        return {'status': 'success', 'error': None}
        
    except Exception as e:
        print(f"❌ Error configurando Django: {str(e)}")
        traceback.print_exc()
        return {'status': 'error', 'error': str(e)}

def generate_report(app_results, model_results, serializer_results, django_result):
    """Generar reporte final"""
    
    print("\n" + "=" * 60)
    print("📊 REPORTE FINAL")
    print("=" * 60)
    
    # Contar resultados
    app_success = sum(1 for r in app_results.values() if r['status'] == 'success')
    app_total = len(app_results)
    
    model_success = sum(1 for r in model_results.values() if r['status'] == 'success')
    model_total = len(model_results)
    
    serializer_success = sum(1 for r in serializer_results.values() if r['status'] == 'success')
    serializer_total = len(serializer_results)
    
    print(f"📦 Apps: {app_success}/{app_total} correctas")
    print(f"🏗️  Modelos: {model_success}/{model_total} correctos")
    print(f"📝 Serializers: {serializer_success}/{serializer_total} correctos")
    print(f"⚙️  Django: {'✅ Correcto' if django_result['status'] == 'success' else '❌ Error'}")
    
    # Mostrar errores
    print(f"\n❌ Errores encontrados:")
    
    for app_name, result in app_results.items():
        if result['status'] == 'error':
            print(f"   📦 {app_name}: {result['error']}")
    
    for model_name, result in model_results.items():
        if result['status'] == 'error':
            print(f"   🏗️  {model_name}: {result['error']}")
    
    for serializer_name, result in serializer_results.items():
        if result['status'] == 'error':
            print(f"   📝 {serializer_name}: {result['error']}")
    
    if django_result['status'] == 'error':
        print(f"   ⚙️  Django: {django_result['error']}")
    
    # Resumen
    total_tests = app_total + model_total + serializer_total + 1
    total_success = app_success + model_success + serializer_success + (1 if django_result['status'] == 'success' else 0)
    
    print(f"\n🎯 Resumen: {total_success}/{total_tests} tests pasaron")
    
    if total_success == total_tests:
        print("🎉 ¡Todos los tests pasaron! El sistema está listo.")
    else:
        print("⚠️  Hay errores que necesitan ser corregidos.")

def main():
    """Función principal"""
    
    print("🚀 Iniciando test completo de importaciones")
    print("=" * 60)
    
    # Ejecutar tests
    app_results = test_app_imports()
    model_results = test_model_imports()
    serializer_results = test_serializer_imports()
    django_result = test_django_setup()
    
    # Generar reporte
    generate_report(app_results, model_results, serializer_results, django_result)

if __name__ == '__main__':
    main() 