#!/usr/bin/env python3
"""
Script para migrar coordenadas y optimizar datos existentes
Migra coordenadas de formato string a decimal y actualiza configuraciones
"""
import os
import sys
import django
from decimal import Decimal
from datetime import date

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings.development')
django.setup()

from api.core.models.catchment_points import (
    CatchmentPoint, 
    ProfileDataConfigCatchment,
    invalidate_telemetry_cache
)


def migrate_coordinates():
    """
    Migrar coordenadas de formato string a decimal
    """
    print("🔄 Migrando coordenadas...")
    
    # Obtener todos los puntos con coordenadas en formato string
    points = CatchmentPoint.objects.filter(
        latitude_old__isnull=False,
        longitude_old__isnull=False
    ).exclude(
        latitude_old='',
        longitude_old=''
    )
    
    migrated_count = 0
    error_count = 0
    
    for point in points:
        try:
            # Convertir coordenadas string a decimal
            lat_str = point.latitude_old.strip()
            lon_str = point.longitude_old.strip()
            
            if lat_str and lon_str:
                try:
                    lat_decimal = Decimal(lat_str)
                    lon_decimal = Decimal(lon_str)
                    
                    # Validar rangos
                    if -90 <= lat_decimal <= 90 and -180 <= lon_decimal <= 180:
                        point.latitude = lat_decimal
                        point.longitude = lon_decimal
                        point.save()
                        migrated_count += 1
                        print(f"✅ Migrado punto {point.id}: {lat_str}, {lon_str} -> {lat_decimal}, {lon_decimal}")
                    else:
                        print(f"⚠️  Coordenadas fuera de rango para punto {point.id}: {lat_str}, {lon_str}")
                        error_count += 1
                        
                except (ValueError, TypeError) as e:
                    print(f"❌ Error convirtiendo coordenadas para punto {point.id}: {lat_str}, {lon_str} - {e}")
                    error_count += 1
            else:
                print(f"⚠️  Coordenadas vacías para punto {point.id}")
                
        except Exception as e:
            print(f"❌ Error procesando punto {point.id}: {e}")
            error_count += 1
    
    print(f"\n📊 Resumen de migración de coordenadas:")
    print(f"   ✅ Migrados: {migrated_count}")
    print(f"   ❌ Errores: {error_count}")
    print(f"   📍 Total procesados: {migrated_count + error_count}")


def optimize_telemetry_configurations():
    """
    Optimizar configuraciones de telemetría existentes
    """
    print("\n🔄 Optimizando configuraciones de telemetría...")
    
    # Obtener configuraciones de datos con telemetría activa
    configs = ProfileDataConfigCatchment.objects.filter(is_telemetry=True)
    
    optimized_count = 0
    
    for config in configs:
        try:
            point = config.point_catchment
            
            if point:
                # Determinar proveedor activo basado en flags
                if point.is_tdata:
                    point.active_provider = 'twin'
                elif point.is_thethings:
                    point.active_provider = 'nettra'
                elif point.is_novus:
                    point.active_provider = 'novus'
                
                # Activar telemetría si tiene configuración
                if config.token_service and point.active_provider:
                    point.is_telemetry_active = True
                    point.telemetry_start_date = config.date_start_telemetry or date.today()
                    point.save()
                    optimized_count += 1
                    print(f"✅ Optimizado punto {point.id}: proveedor={point.active_provider}")
                
        except Exception as e:
            print(f"❌ Error optimizando configuración {config.id}: {e}")
    
    print(f"\n📊 Resumen de optimización:")
    print(f"   ✅ Optimizados: {optimized_count}")


def update_variable_configurations():
    """
    Actualizar configuraciones de variables para usar esquemas dinámicos
    """
    print("\n🔄 Actualizando configuraciones de variables...")
    
    # Obtener puntos con telemetría activa
    active_points = CatchmentPoint.objects.filter(is_telemetry_active=True)
    
    updated_count = 0
    
    for point in active_points:
        try:
            # Obtener configuración actual
            config = point.get_telemetry_config()
            
            if config:
                # Crear configuración de variables estándar
                variables_config = {
                    'level': {
                        'enabled': True,
                        'unit': 'm',
                        'min_value': 0,
                        'max_value': 100,
                        'processing': {
                            'calculate_nivel': config.get('d3', 0)
                        }
                    },
                    'flow': {
                        'enabled': True,
                        'unit': 'l/s',
                        'min_value': 0,
                        'max_value': 1000,
                        'processing': {
                            'convert_to_lt': True
                        }
                    },
                    'total': {
                        'enabled': True,
                        'unit': 'm3',
                        'min_value': 0,
                        'processing': {
                            'pulses_factor': config.get('d6', 1000),
                            'addition': 0
                        }
                    }
                }
                
                # Actualizar configuración
                config['variables'] = variables_config
                
                # Guardar en cache
                from django.core.cache import cache
                cache_key = f'telemetry_config_{point.pk}'
                cache.set(cache_key, config, timeout=1800)
                
                updated_count += 1
                print(f"✅ Actualizada configuración de variables para punto {point.id}")
                
        except Exception as e:
            print(f"❌ Error actualizando variables para punto {point.id}: {e}")
    
    print(f"\n📊 Resumen de actualización de variables:")
    print(f"   ✅ Actualizados: {updated_count}")


def create_spatial_indexes():
    """
    Crear índices espaciales para optimizar consultas geográficas
    """
    print("\n🔄 Creando índices espaciales...")
    
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Crear índice espacial en el campo location
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_catchment_point_location 
                ON core_catchmentpoint USING GIST (location);
            """)
            
            # Crear índice en coordenadas
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_catchment_point_coordinates 
                ON core_catchmentpoint (latitude, longitude);
            """)
            
            print("✅ Índices espaciales creados exitosamente")
            
    except Exception as e:
        print(f"❌ Error creando índices espaciales: {e}")


def validate_migration():
    """
    Validar que la migración fue exitosa
    """
    print("\n🔍 Validando migración...")
    
    # Verificar puntos con coordenadas decimales
    decimal_coords = CatchmentPoint.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).count()
    
    # Verificar puntos con telemetría activa
    active_telemetry = CatchmentPoint.objects.filter(
        is_telemetry_active=True
    ).count()
    
    # Verificar puntos con proveedor activo
    with_provider = CatchmentPoint.objects.filter(
        active_provider__isnull=False
    ).exclude(active_provider='').count()
    
    print(f"📊 Estadísticas de validación:")
    print(f"   📍 Puntos con coordenadas decimales: {decimal_coords}")
    print(f"   📡 Puntos con telemetría activa: {active_telemetry}")
    print(f"   🔌 Puntos con proveedor activo: {with_provider}")
    
    # Verificar configuración de variables
    configs_with_vars = 0
    for point in CatchmentPoint.objects.filter(is_telemetry_active=True):
        config = point.get_telemetry_config()
        if config and config.get('variables'):
            configs_with_vars += 1
    
    print(f"   ⚙️  Puntos con configuración de variables: {configs_with_vars}")


def main():
    """
    Función principal de migración
    """
    print("🚀 Iniciando migración de coordenadas y optimización de telemetría")
    print("=" * 60)
    
    try:
        # 1. Migrar coordenadas
        migrate_coordinates()
        
        # 2. Optimizar configuraciones de telemetría
        optimize_telemetry_configurations()
        
        # 3. Actualizar configuraciones de variables
        update_variable_configurations()
        
        # 4. Crear índices espaciales
        create_spatial_indexes()
        
        # 5. Invalidar cache
        print("\n🔄 Invalidando cache...")
        invalidate_telemetry_cache()
        print("✅ Cache invalidado")
        
        # 6. Validar migración
        validate_migration()
        
        print("\n🎉 Migración completada exitosamente!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 