#!/usr/bin/env python3
"""
Script para probar la arquitectura de dos capas
"""
import os
import sys
import django
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.config.settings.development')
django.setup()

from api.apps.variables.models.variables.variable import Variable
from api.apps.variables.models.schemas.schema import VariableSchema
from api.apps.catchment.models.points.catchment_point import CatchmentPoint
from api.apps.telemetry.models.data.telemetry_data import TelemetryData


def test_arquitectura_dos_capas():
    """Probar la arquitectura de dos capas"""
    print("🧪 Probando Arquitectura de Dos Capas")
    print("=" * 50)
    
    # 1. Verificar que las apps están configuradas
    print("\n1. ✅ Verificando configuración de apps...")
    try:
        from django.conf import settings
        apps = [app for app in settings.INSTALLED_APPS if 'api.apps' in app]
        print(f"   Apps encontradas: {len(apps)}")
        for app in apps:
            print(f"   - {app}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # 2. Verificar que los serializers existen
    print("\n2. ✅ Verificando serializers...")
    try:
        from api.apps.core.api.base.serializers.base_serializers import (
            VariableBaseSerializer, VariableSchemaBaseSerializer
        )
        from api.apps.frontend.api.serializers.frontend_serializers import (
            VariableFrontendSerializer, VariableSchemaFrontendSerializer
        )
        print("   ✅ Serializers base importados correctamente")
        print("   ✅ Serializers frontend importados correctamente")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # 3. Verificar que los ViewSets existen
    print("\n3. ✅ Verificando ViewSets...")
    try:
        from api.apps.core.api.base.views.base_viewsets import (
            VariableBaseViewSet, VariableSchemaBaseViewSet
        )
        from api.apps.frontend.api.views.frontend_viewsets import (
            VariableFrontendViewSet, VariableSchemaFrontendViewSet
        )
        print("   ✅ ViewSets base importados correctamente")
        print("   ✅ ViewSets frontend importados correctamente")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # 4. Verificar URLs
    print("\n4. ✅ Verificando URLs...")
    try:
        from api.config.urls.base import urlpatterns as base_urls
        from api.config.urls.frontend import urlpatterns as frontend_urls
        print(f"   ✅ URLs base: {len(base_urls)} patrones")
        print(f"   ✅ URLs frontend: {len(frontend_urls)} patrones")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # 5. Verificar modelos
    print("\n5. ✅ Verificando modelos...")
    try:
        # Verificar que los modelos existen
        variable_count = Variable.objects.count()
        schema_count = VariableSchema.objects.count()
        point_count = CatchmentPoint.objects.count()
        telemetry_count = TelemetryData.objects.count()
        
        print(f"   ✅ Variables: {variable_count}")
        print(f"   ✅ Esquemas: {schema_count}")
        print(f"   ✅ Puntos de captación: {point_count}")
        print(f"   ✅ Datos de telemetría: {telemetry_count}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # 6. Probar serializers
    print("\n6. ✅ Probando serializers...")
    try:
        # Crear datos de prueba
        variable = Variable.objects.create(
            name="Variable de Prueba",
            code="TEST_001",
            variable_type="NIVEL",
            unit="METERS"
        )
        
        # Probar serializer base
        base_serializer = VariableBaseSerializer(variable)
        base_data = base_serializer.data
        print(f"   ✅ Serializer base: {len(base_data)} campos")
        
        # Probar serializer frontend
        frontend_serializer = VariableFrontendSerializer(variable)
        frontend_data = frontend_serializer.data
        print(f"   ✅ Serializer frontend: {len(frontend_data)} campos")
        
        # Verificar campos adicionales
        additional_fields = set(frontend_data.keys()) - set(base_data.keys())
        print(f"   ✅ Campos adicionales: {additional_fields}")
        
        # Limpiar
        variable.delete()
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n🎉 ¡Arquitectura de dos capas funcionando correctamente!")
    return True


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


def mostrar_ejemplos_uso():
    """Mostrar ejemplos de uso"""
    print("\n📖 Ejemplos de Uso")
    print("=" * 50)
    
    print("\n1. Crear variable (API Base):")
    print("""
    POST /api/base/variables/
    {
        "name": "Nivel de Agua",
        "code": "NIVEL_001",
        "variable_type": "NIVEL",
        "unit": "METERS"
    }
    """)
    
    print("\n2. Consultar variable (API Frontend):")
    print("""
    GET /api/frontend/variables/1/
    
    Respuesta:
    {
        "id": 1,
        "name": "Nivel de Agua",
        "code": "NIVEL_001",
        "display_name": "Nivel de Agua del Pozo",
        "unit_display": "metros",
        "status_display": "Activa",
        "variable_type_display": "Nivel"
    }
    """)
    
    print("\n3. Dashboard con caché:")
    print("""
    GET /api/frontend/variables/dashboard_summary/
    
    Respuesta:
    {
        "total_variables": 25,
        "active_variables": 23,
        "variables_by_type": [...],
        "recent_variables": [...]
    }
    """)


if __name__ == "__main__":
    print("🚀 Iniciando pruebas de arquitectura...")
    
    # Ejecutar pruebas
    success = test_arquitectura_dos_capas()
    
    if success:
        # Mostrar información adicional
        mostrar_endpoints()
        mostrar_ejemplos_uso()
        
        print("\n✅ ¡Todas las pruebas pasaron!")
        print("🎯 La arquitectura de dos capas está lista para usar.")
    else:
        print("\n❌ Algunas pruebas fallaron.")
        print("🔧 Revisa los errores y corrige los problemas.")
        sys.exit(1) 