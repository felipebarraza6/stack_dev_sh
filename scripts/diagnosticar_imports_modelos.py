#!/usr/bin/env python3
"""
Script para diagnosticar y corregir imports de modelos
Verifica que todos los modelos estén correctamente importados en los __init__.py
"""

import os
import sys
import importlib
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.config.settings.development')

import django
django.setup()

from django.apps import apps


def verificar_modelos_existentes():
    """Verifica qué modelos existen realmente en el sistema"""
    print("🔍 Verificando modelos existentes...")
    
    modelos_encontrados = {}
    
    # Apps principales
    apps_to_check = [
        'api.apps.core',
        'api.apps.catchment', 
        'api.apps.telemetry',
        'api.apps.compliance',
        'api.apps.variables',
        'api.apps.providers',
        'api.apps.users',
    ]
    
    for app_name in apps_to_check:
        try:
            app = apps.get_app_config(app_name.split('.')[-1])
            modelos_encontrados[app_name] = []
            
            # Buscar archivos de modelos
            models_dir = Path(app.path) / 'models'
            if models_dir.exists():
                for model_file in models_dir.rglob('*.py'):
                    if model_file.name != '__init__.py':
                        # Intentar importar el archivo
                        try:
                            module_path = f"{app_name}.models.{model_file.relative_to(models_dir.parent).with_suffix('').as_posix().replace('/', '.')}"
                            module = importlib.import_module(module_path)
                            
                            # Buscar clases de modelo en el módulo
                            for attr_name in dir(module):
                                attr = getattr(module, attr_name)
                                if hasattr(attr, '_meta') and hasattr(attr._meta, 'app_label'):
                                    if attr._meta.app_label == app.label:
                                        modelos_encontrados[app_name].append(attr_name)
                                        print(f"   ✅ {app_name}.{attr_name}")
                        except Exception as e:
                            print(f"   ⚠️  Error importando {model_file}: {e}")
                            
        except Exception as e:
            print(f"   ❌ Error con app {app_name}: {e}")
    
    return modelos_encontrados


def verificar_imports_actuales():
    """Verifica qué imports están actualmente activos"""
    print("\n📋 Verificando imports actuales...")
    
    imports_actuales = {}
    
    # Archivos __init__.py a verificar
    init_files = [
        'api/apps/core/__init__.py',
        'api/apps/catchment/__init__.py',
        'api/apps/telemetry/__init__.py',
        'api/apps/compliance/__init__.py',
        'api/apps/variables/__init__.py',
        'api/apps/providers/__init__.py',
        'api/apps/users/__init__.py',
    ]
    
    for init_file in init_files:
        if os.path.exists(init_file):
            with open(init_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Buscar imports comentados y activos
            imports_actuales[init_file] = {
                'comentados': [],
                'activos': []
            }
            
            lines = content.split('\n')
            for line in lines:
                if line.strip().startswith('# from'):
                    # Import comentado
                    import_line = line.strip()[2:]  # Remover #
                    if 'import' in import_line:
                        imports_actuales[init_file]['comentados'].append(import_line)
                elif line.strip().startswith('from') and 'import' in line:
                    # Import activo
                    imports_actuales[init_file]['activos'].append(line.strip())
            
            print(f"   📁 {init_file}")
            print(f"      Activos: {len(imports_actuales[init_file]['activos'])}")
            print(f"      Comentados: {len(imports_actuales[init_file]['comentados'])}")
    
    return imports_actuales


def generar_imports_corregidos():
    """Genera los imports corregidos para cada app"""
    print("\n🔧 Generando imports corregidos...")
    
    # Mapeo de modelos por app
    modelos_por_app = {
        'api/apps/core/__init__.py': {
            'imports': [
                'from .models.base import BaseModel, TimestampedModel, SoftDeleteModel'
            ],
            'exports': ['BaseModel', 'TimestampedModel', 'SoftDeleteModel']
        },
        
        'api/apps/catchment/__init__.py': {
            'imports': [
                'from .models.points.catchment_point import CatchmentPoint',
                'from .models.configs.processing_config import CatchmentPointProcessingConfig',
                'from .models.notifications.notification import CatchmentPointNotification'
            ],
            'exports': ['CatchmentPoint', 'CatchmentPointProcessingConfig', 'CatchmentPointNotification']
        },
        
        'api/apps/telemetry/__init__.py': {
            'imports': [
                'from .models.models import (',
                '    TelemetryData, TelemetryNotification, TelemetryNotificationResponse,',
                '    TelemetryProcessingLog, RawTelemetryData, ResponseSchema,',
                '    ProcessingConstant, ProcessedTelemetryData',
                ')'
            ],
            'exports': [
                'TelemetryData', 'TelemetryNotification', 'TelemetryNotificationResponse',
                'TelemetryProcessingLog', 'RawTelemetryData', 'ResponseSchema',
                'ProcessingConstant', 'ProcessedTelemetryData'
            ]
        },
        
        'api/apps/compliance/__init__.py': {
            'imports': [
                'from .models.configs.compliance_config import ComplianceConfig',
                'from .models.sources.compliance_source import ComplianceSource',
                'from .models.data.compliance_data import ComplianceData'
            ],
            'exports': ['ComplianceConfig', 'ComplianceSource', 'ComplianceData']
        },
        
        'api/apps/variables/__init__.py': {
            'imports': [
                'from .models.variables.variable import Variable',
                'from .models.schemas.schema import VariableSchema',
                'from .models.schemas.mapping import VariableSchemaMapping',
                'from .models.data_points.data_point import VariableDataPoint',
                'from .models.alerts.alert import VariableAlert',
                'from .models.alerts.alert_log import VariableAlertLog'
            ],
            'exports': [
                'Variable', 'VariableSchema', 'VariableSchemaMapping',
                'VariableDataPoint', 'VariableAlert', 'VariableAlertLog'
            ]
        },
        
        'api/apps/providers/__init__.py': {
            'imports': [
                'from .models.providers.provider import Provider, ProviderSchemaMapping',
                'from .models.mqtt.broker import MQTTBroker',
                'from .models.tokens.device_token import DeviceToken',
                'from .models.schemas.data_schema import DataSchema',
                'from .models.logs.ingestion_log import DataIngestionLog'
            ],
            'exports': [
                'Provider', 'ProviderSchemaMapping', 'MQTTBroker', 'DeviceToken',
                'DataSchema', 'DataIngestionLog'
            ]
        },
        
        'api/apps/users/__init__.py': {
            'imports': [
                'from .models.users.user import User'
            ],
            'exports': ['User']
        }
    }
    
    return modelos_por_app


def corregir_imports():
    """Corrige los imports en los archivos __init__.py"""
    print("\n🛠️  Corrigiendo imports...")
    
    modelos_por_app = generar_imports_corregidos()
    
    for init_file, config in modelos_por_app.items():
        if os.path.exists(init_file):
            print(f"   📝 Corrigiendo {init_file}")
            
            # Leer contenido actual
            with open(init_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generar nuevo contenido
            new_content = f'''"""
{os.path.basename(os.path.dirname(init_file)).title()} App
"""

default_app_config = 'api.apps.{os.path.basename(os.path.dirname(init_file)).lower()}.apps.{os.path.basename(os.path.dirname(init_file)).title()}AppConfig'

# Importar modelos
{chr(10).join(config['imports'])}

# Importar serializers (comentado por ahora)
# from .serializers.serializers import *

__all__ = [
{chr(10).join(f"    '{export}'," for export in config['exports'])}
]
'''
            
            # Escribir nuevo contenido
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"      ✅ Corregido")


def verificar_imports_funcionando():
    """Verifica que los imports funcionen correctamente"""
    print("\n✅ Verificando que los imports funcionen...")
    
    try:
        # Intentar importar modelos de cada app
        from api.apps.core import BaseModel, TimestampedModel, SoftDeleteModel
        print("   ✅ Core models importados correctamente")
        
        from api.apps.catchment import CatchmentPoint
        print("   ✅ Catchment models importados correctamente")
        
        from api.apps.telemetry import TelemetryData
        print("   ✅ Telemetry models importados correctamente")
        
        from api.apps.compliance import ComplianceConfig
        print("   ✅ Compliance models importados correctamente")
        
        from api.apps.variables import Variable
        print("   ✅ Variables models importados correctamente")
        
        from api.apps.providers import Provider
        print("   ✅ Providers models importados correctamente")
        
        print("\n🎉 Todos los imports funcionan correctamente!")
        return True
        
    except ImportError as e:
        print(f"   ❌ Error de import: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
        return False


def main():
    """Función principal"""
    print("🚀 Diagnóstico de Imports de Modelos")
    print("=" * 50)
    
    # Paso 1: Verificar modelos existentes
    modelos_encontrados = verificar_modelos_existentes()
    
    # Paso 2: Verificar imports actuales
    imports_actuales = verificar_imports_actuales()
    
    # Paso 3: Corregir imports
    corregir_imports()
    
    # Paso 4: Verificar que funcionen
    if verificar_imports_funcionando():
        print("\n📋 Resumen:")
        print("   ✅ Imports corregidos exitosamente")
        print("   ✅ Modelos disponibles para importar desde vistas, serializers, signals, etc.")
        print("\n💡 Ahora puedes usar:")
        print("   from api.apps.telemetry import TelemetryData")
        print("   from api.apps.catchment import CatchmentPoint")
        print("   from api.apps.compliance import ComplianceConfig")
        print("   # etc...")
    else:
        print("\n❌ Hay errores en los imports que necesitan atención manual")


if __name__ == '__main__':
    main() 