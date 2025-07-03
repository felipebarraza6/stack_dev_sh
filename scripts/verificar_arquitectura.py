#!/usr/bin/env python3
"""
Script simple para verificar la arquitectura de dos capas
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.config.settings.development')
django.setup()

def verificar_imports():
    """Verificar que todos los imports funcionan"""
    print("🧪 Verificando imports de la arquitectura...")
    print("=" * 50)
    
    try:
        # Verificar serializers base
        print("\n1. ✅ Verificando serializers base...")
        from api.apps.core.api.base.serializers.base_serializers import (
            BaseModelSerializer,
            VariableBaseSerializer,
            VariableSchemaBaseSerializer,
            CatchmentPointBaseSerializer,
            TelemetryDataBaseSerializer
        )
        print("   ✅ Todos los serializers base importados correctamente")
        
        # Verificar serializers frontend
        print("\n2. ✅ Verificando serializers frontend...")
        from api.apps.frontend.api.serializers.frontend_serializers import (
            VariableFrontendSerializer,
            VariableSchemaFrontendSerializer,
            CatchmentPointFrontendSerializer,
            TelemetryDataFrontendSerializer
        )
        print("   ✅ Todos los serializers frontend importados correctamente")
        
        # Verificar ViewSets base
        print("\n3. ✅ Verificando ViewSets base...")
        from api.apps.core.api.base.views.base_viewsets import (
            BaseModelViewSet,
            VariableBaseViewSet,
            VariableSchemaBaseViewSet,
            CatchmentPointBaseViewSet,
            TelemetryDataBaseViewSet
        )
        print("   ✅ Todos los ViewSets base importados correctamente")
        
        # Verificar ViewSets frontend
        print("\n4. ✅ Verificando ViewSets frontend...")
        from api.apps.frontend.api.views.frontend_viewsets import (
            VariableFrontendViewSet,
            VariableSchemaFrontendViewSet,
            CatchmentPointFrontendViewSet,
            TelemetryDataFrontendViewSet
        )
        print("   ✅ Todos los ViewSets frontend importados correctamente")
        
        # Verificar URLs
        print("\n5. ✅ Verificando URLs...")
        from api.config.urls.base import urlpatterns as base_urls
        from api.config.urls.frontend import urlpatterns as frontend_urls
        print(f"   ✅ URLs base: {len(base_urls)} patrones")
        print(f"   ✅ URLs frontend: {len(frontend_urls)} patrones")
        
        # Verificar apps
        print("\n6. ✅ Verificando apps...")
        from django.conf import settings
        apps = [app for app in settings.INSTALLED_APPS if 'api.apps' in app]
        print(f"   ✅ Apps encontradas: {len(apps)}")
        for app in apps:
            print(f"   - {app}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def mostrar_estructura():
    """Mostrar estructura de la arquitectura"""
    print("\n🏗️ Estructura de la Arquitectura")
    print("=" * 50)
    
    print("""
    api/
    ├── apps/
    │   ├── core/
    │   │   └── api/
    │   │       └── base/                    # 🔧 API Base (Servicio Interno)
    │   │           ├── serializers/
    │   │           │   ├── __init__.py
    │   │           │   └── base_serializers.py
    │   │           └── views/
    │   │               ├── __init__.py
    │   │               └── base_viewsets.py
    │   └── frontend/
    │       └── api/                         # 🎨 API Frontend (Capa Externa)
    │           ├── serializers/
    │           │   ├── __init__.py
    │           │   └── frontend_serializers.py
    │           └── views/
    │               ├── __init__.py
    │               └── frontend_viewsets.py
    └── config/
        └── urls/
            ├── base.py                      # URLs API Base
            └── frontend.py                  # URLs API Frontend
    """)

def mostrar_endpoints():
    """Mostrar endpoints disponibles"""
    print("\n📋 Endpoints Disponibles")
    print("=" * 50)
    
    print("\n🔧 API Base (Servicio Interno):")
    print("   GET    /api/base/variables/")
    print("   POST   /api/base/variables/")
    print("   GET    /api/base/variables/{id}/")
    print("   PUT    /api/base/variables/{id}/")
    print("   DELETE /api/base/variables/{id}/")
    print("   GET    /api/base/variables/active_count/")
    
    print("\n🎨 API Frontend (Capa Externa):")
    print("   GET    /api/frontend/variables/")
    print("   GET    /api/frontend/variables/{id}/")
    print("   GET    /api/frontend/variables/dashboard_summary/")
    print("   GET    /api/frontend/schemas/")
    print("   POST   /api/frontend/schemas/{id}/assign_to_catchment_point/")
    print("   GET    /api/frontend/catchment-points/map_data/")
    print("   GET    /api/frontend/telemetry-data/latest_summary/")
    print("   GET    /api/frontend/telemetry-data/chart_data/")

def mostrar_beneficios():
    """Mostrar beneficios de la arquitectura"""
    print("\n🎯 Beneficios de la Arquitectura")
    print("=" * 50)
    
    print("\n✅ Para el Sistema Base:")
    print("   - API estable para servicios internos")
    print("   - Sin dependencias de frontend")
    print("   - Fácil testing y mantenimiento")
    print("   - Cache independiente")
    
    print("\n✅ Para el Frontend:")
    print("   - Flexibilidad total en serializers")
    print("   - Campos adicionales (labels, etc.)")
    print("   - Optimizaciones específicas")
    print("   - Cache separado")
    
    print("\n✅ Para el Desarrollo:")
    print("   - Separación clara de responsabilidades")
    print("   - Fácil evolución independiente")
    print("   - Testing aislado")
    print("   - Deployment independiente")

if __name__ == "__main__":
    print("🚀 Verificando Arquitectura de Dos Capas...")
    
    # Verificar imports
    success = verificar_imports()
    
    if success:
        print("\n🎉 ¡Arquitectura verificada exitosamente!")
        
        # Mostrar información adicional
        mostrar_estructura()
        mostrar_endpoints()
        mostrar_beneficios()
        
        print("\n✅ ¡La arquitectura de dos capas está lista para usar!")
        print("🎯 Puedes empezar a usar los endpoints inmediatamente.")
    else:
        print("\n❌ Algunas verificaciones fallaron.")
        print("🔧 Revisa los errores y corrige los problemas.")
        sys.exit(1) 