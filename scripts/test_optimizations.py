#!/usr/bin/env python3
"""
Script para probar las optimizaciones de telemetría
Verifica el rendimiento y funcionalidad de las mejoras
"""
import os
import sys
import time
import asyncio
import requests
from datetime import datetime
import pytz

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings.development')

import django
django.setup()

from api.core.models.catchment_points import (
    get_active_telemetry_points,
    get_points_by_frequency,
    get_points_by_provider,
    invalidate_telemetry_cache
)

CHILE_TZ = pytz.timezone('America/Santiago')


def test_cache_performance():
    """
    Probar rendimiento del cache
    """
    print("🧪 Probando rendimiento del cache...")
    
    # Primera consulta (sin cache)
    start_time = time.time()
    points_1 = get_active_telemetry_points()
    first_query_time = time.time() - start_time
    
    # Segunda consulta (con cache)
    start_time = time.time()
    points_2 = get_active_telemetry_points()
    second_query_time = time.time() - start_time
    
    # Tercera consulta (con cache)
    start_time = time.time()
    points_3 = get_active_telemetry_points()
    third_query_time = time.time() - start_time
    
    print(f"   ⏱️  Primera consulta: {first_query_time:.4f}s")
    print(f"   ⚡ Segunda consulta: {second_query_time:.4f}s")
    print(f"   ⚡ Tercera consulta: {third_query_time:.4f}s")
    
    improvement = (first_query_time - second_query_time) / first_query_time * 100
    print(f"   📈 Mejora de rendimiento: {improvement:.1f}%")
    
    # Verificar consistencia
    if len(points_1) == len(points_2) == len(points_3):
        print(f"   ✅ Consistencia del cache: OK ({len(points_1)} puntos)")
    else:
        print(f"   ❌ Inconsistencia en el cache detectada")


def test_frequency_queries():
    """
    Probar consultas por frecuencia
    """
    print("\n🧪 Probando consultas por frecuencia...")
    
    frequencies = ['1', '5', '60']
    
    for freq in frequencies:
        start_time = time.time()
        points = get_points_by_frequency(freq)
        query_time = time.time() - start_time
        
        print(f"   📡 Frecuencia {freq}min: {len(points)} puntos en {query_time:.4f}s")


def test_provider_queries():
    """
    Probar consultas por proveedor
    """
    print("\n🧪 Probando consultas por proveedor...")
    
    providers = ['twin', 'nettra', 'novus']
    
    for provider in providers:
        start_time = time.time()
        points = get_points_by_provider(provider)
        query_time = time.time() - start_time
        
        print(f"   🔌 Proveedor {provider}: {len(points)} puntos en {query_time:.4f}s")


def test_coordinates_validation():
    """
    Probar validación de coordenadas
    """
    print("\n🧪 Probando validación de coordenadas...")
    
    from api.core.models.catchment_points import CatchmentPoint
    
    # Puntos con coordenadas decimales
    decimal_coords = CatchmentPoint.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).count()
    
    # Puntos con coordenadas válidas
    valid_coords = 0
    invalid_coords = 0
    
    for point in CatchmentPoint.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    )[:10]:  # Probar solo los primeros 10
        try:
            coords = point.coordinates
            if coords:
                lat, lon = coords
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    valid_coords += 1
                else:
                    invalid_coords += 1
            else:
                invalid_coords += 1
        except Exception:
            invalid_coords += 1
    
    print(f"   📍 Puntos con coordenadas decimales: {decimal_coords}")
    print(f"   ✅ Coordenadas válidas: {valid_coords}")
    print(f"   ❌ Coordenadas inválidas: {invalid_coords}")


def test_telemetry_config():
    """
    Probar configuración de telemetría
    """
    print("\n🧪 Probando configuración de telemetría...")
    
    from api.core.models.catchment_points import CatchmentPoint
    
    # Puntos con telemetría activa
    active_points = CatchmentPoint.objects.filter(is_telemetry_active=True)
    
    ready_points = 0
    not_ready_points = 0
    
    for point in active_points[:10]:  # Probar solo los primeros 10
        try:
            if point.is_ready_for_telemetry:
                ready_points += 1
                config = point.get_telemetry_config()
                if config:
                    print(f"   ✅ Punto {point.id}: {point.active_provider} - {point.frecuency}min")
                else:
                    print(f"   ⚠️  Punto {point.id}: Sin configuración")
            else:
                not_ready_points += 1
        except Exception as e:
            print(f"   ❌ Error en punto {point.id}: {e}")
    
    print(f"   📡 Puntos listos para telemetría: {ready_points}")
    print(f"   ⚠️  Puntos no listos: {not_ready_points}")


def test_cache_invalidation():
    """
    Probar invalidación de cache
    """
    print("\n🧪 Probando invalidación de cache...")
    
    # Consulta inicial
    points_before = get_active_telemetry_points()
    print(f"   📊 Puntos antes de invalidación: {len(points_before)}")
    
    # Invalidar cache
    start_time = time.time()
    invalidate_telemetry_cache()
    invalidation_time = time.time() - start_time
    
    # Consulta después de invalidación
    points_after = get_active_telemetry_points()
    print(f"   📊 Puntos después de invalidación: {len(points_after)}")
    print(f"   ⏱️  Tiempo de invalidación: {invalidation_time:.4f}s")
    
    if len(points_before) == len(points_after):
        print("   ✅ Invalidación exitosa")
    else:
        print("   ❌ Error en invalidación")


def test_api_endpoints():
    """
    Probar endpoints de la API
    """
    print("\n🧪 Probando endpoints de la API...")
    
    base_url = "http://localhost:8001"
    endpoints = [
        "/",
        "/health",
        "/ready",
        "/stats",
        "/points/active",
        "/metrics"
    ]
    
    for endpoint in endpoints:
        try:
            start_time = time.time()
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                print(f"   ✅ {endpoint}: {response.status_code} ({response_time:.3f}s)")
            else:
                print(f"   ❌ {endpoint}: {response.status_code} ({response_time:.3f}s)")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {endpoint}: Error - {e}")


def test_memory_usage():
    """
    Probar uso de memoria
    """
    print("\n🧪 Probando uso de memoria...")
    
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss / 1024 / 1024  # MB
    
    # Realizar múltiples consultas
    for i in range(100):
        get_active_telemetry_points()
        if i % 20 == 0:
            print(f"   🔄 Consulta {i+1}/100")
    
    memory_after = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = memory_after - memory_before
    
    print(f"   💾 Memoria antes: {memory_before:.1f}MB")
    print(f"   💾 Memoria después: {memory_after:.1f}MB")
    print(f"   📈 Incremento: {memory_increase:.1f}MB")
    
    if memory_increase < 50:  # Menos de 50MB de incremento
        print("   ✅ Uso de memoria: OK")
    else:
        print("   ⚠️  Uso de memoria: Alto")


def generate_performance_report():
    """
    Generar reporte de rendimiento
    """
    print("\n📊 Generando reporte de rendimiento...")
    
    from api.core.models.catchment_points import CatchmentPoint
    
    # Estadísticas generales
    total_points = CatchmentPoint.objects.count()
    active_points = CatchmentPoint.objects.filter(is_telemetry_active=True).count()
    points_with_coords = CatchmentPoint.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).count()
    
    # Estadísticas por proveedor
    providers = {}
    for point in CatchmentPoint.objects.filter(is_telemetry_active=True):
        provider = point.active_provider
        if provider:
            providers[provider] = providers.get(provider, 0) + 1
    
    # Estadísticas por frecuencia
    frequencies = {}
    for point in CatchmentPoint.objects.filter(is_telemetry_active=True):
        freq = point.frecuency
        if freq:
            frequencies[freq] = frequencies.get(freq, 0) + 1
    
    report = {
        "timestamp": datetime.now(CHILE_TZ).isoformat(),
        "total_points": total_points,
        "active_telemetry": active_points,
        "points_with_coordinates": points_with_coords,
        "providers": providers,
        "frequencies": frequencies,
        "estimated_measurements_per_hour": sum(
            count * (60 if freq == '1' else 12 if freq == '5' else 1)
            for freq, count in frequencies.items()
        )
    }
    
    print("   📈 Reporte de rendimiento:")
    print(f"      Total de puntos: {report['total_points']}")
    print(f"      Telemetría activa: {report['active_telemetry']}")
    print(f"      Con coordenadas: {report['points_with_coordinates']}")
    print(f"      Proveedores: {report['providers']}")
    print(f"      Frecuencias: {report['frequencies']}")
    print(f"      Mediciones/hora estimadas: {report['estimated_measurements_per_hour']}")
    
    return report


def main():
    """
    Función principal de pruebas
    """
    print("🧪 Iniciando pruebas de optimización de telemetría")
    print("=" * 60)
    
    try:
        # Ejecutar todas las pruebas
        test_cache_performance()
        test_frequency_queries()
        test_provider_queries()
        test_coordinates_validation()
        test_telemetry_config()
        test_cache_invalidation()
        test_memory_usage()
        
        # Generar reporte final
        report = generate_performance_report()
        
        print("\n🎉 Pruebas completadas exitosamente!")
        print("=" * 60)
        
        # Guardar reporte
        import json
        with open('performance_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print("📄 Reporte guardado en performance_report.json")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 