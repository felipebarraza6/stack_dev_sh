#!/usr/bin/env python
"""
Script para configurar la conversión de pulsos en el sistema
Configura variables y puntos de captación con las constantes de pulsos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.config.settings.development')
django.setup()

from api.apps.variables.models import Variable
from api.apps.catchment.models import CatchmentPoint
from api.apps.users.models import User
from api.apps.telemetry.processors.processor import TelemetryProcessor


def create_variables():
    """Crear variables con configuración de procesamiento"""
    print("🔧 Creando variables...")
    
    # Variable Totalizado
    total_var, created = Variable.objects.get_or_create(
        code="total",
        defaults={
            "name": "Totalizado de Agua",
            "variable_type": "TOTALIZADO",
            "unit": "CUBIC_METERS",
            "min_value": 0.0,
            "max_value": 999999.0,
            "processing_config": {
                "rules": [
                    {
                        "type": "pulse_conversion",
                        "pulses_per_liter": 1000,
                        "target_unit": "m³",
                        "description": "Convertir pulsos a metros cúbicos"
                    },
                    {
                        "type": "reset_on_threshold",
                        "threshold": 0.0,
                        "reset_value": 0.0,
                        "condition": "eq",
                        "description": "Resetear cuando total llega a 0"
                    }
                ],
                "calibration_factor": 1.023,
                "alert_threshold": None
            },
            "alert_config": {
                "enabled": False,
                "min_threshold": None,
                "max_threshold": None
            }
        }
    )
    
    if created:
        print(f"✅ Variable 'total' creada")
    else:
        print(f"ℹ️  Variable 'total' ya existe")
    
    # Variable Caudal
    flow_var, created = Variable.objects.get_or_create(
        code="flow",
        defaults={
            "name": "Caudal Instantáneo",
            "variable_type": "CAUDAL",
            "unit": "LITERS_PER_SECOND",
            "min_value": 0.0,
            "max_value": 1000.0,
            "processing_config": {
                "rules": [
                    {
                        "type": "range_validation",
                        "min": 0.0,
                        "max": 1000.0,
                        "description": "Validar rango de caudal"
                    },
                    {
                        "type": "calibration",
                        "factor": 1.015,
                        "description": "Factor de calibración"
                    }
                ],
                "alert_threshold": 0.0
            },
            "alert_config": {
                "enabled": True,
                "min_threshold": 0.1,
                "max_threshold": 1000.0
            }
        }
    )
    
    if created:
        print(f"✅ Variable 'flow' creada")
    else:
        print(f"ℹ️  Variable 'flow' ya existe")
    
    # Variable Nivel
    level_var, created = Variable.objects.get_or_create(
        code="level",
        defaults={
            "name": "Nivel Freático",
            "variable_type": "NIVEL",
            "unit": "METERS",
            "min_value": 0.0,
            "max_value": 100.0,
            "processing_config": {
                "rules": [
                    {
                        "type": "range_validation",
                        "min": 0.0,
                        "max": 100.0,
                        "description": "Validar rango de nivel"
                    },
                    {
                        "type": "reset_on_threshold",
                        "threshold": 95.0,
                        "reset_value": 0.0,
                        "condition": "gte",
                        "description": "Resetear cuando nivel supera 95m"
                    }
                ],
                "alert_threshold": 90.0
            },
            "alert_config": {
                "enabled": True,
                "min_threshold": 0.0,
                "max_threshold": 90.0
            }
        }
    )
    
    if created:
        print(f"✅ Variable 'level' creada")
    else:
        print(f"ℹ️  Variable 'level' ya existe")
    
    return total_var, flow_var, level_var


def configure_catchment_points():
    """Configurar puntos de captación con constantes de pulsos"""
    print("\n🏞️ Configurando puntos de captación...")
    
    # Obtener o crear usuario propietario
    try:
        owner = User.objects.first()
        if not owner:
            owner = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123',
                is_staff=True,
                is_superuser=True
            )
            print(f"✅ Usuario admin creado")
    except Exception as e:
        print(f"⚠️  Error con usuario: {e}")
        return
    
    # Configurar puntos existentes o crear uno de ejemplo
    points = CatchmentPoint.objects.all()
    
    if not points.exists():
        # Crear punto de ejemplo
        point = CatchmentPoint.objects.create(
            name="Pozo Principal",
            code="POZO_001",
            point_type="WELL",
            owner=owner,
            latitude=-33.4489,
            longitude=-70.6693,
            altitude=520.0,
            device_id="DEV001",
            provider="twin",
            status="ACTIVE",
            sampling_frequency=60,
            config={
                "pulse_constants": {
                    "total": {
                        "pulses_per_liter": 1000,
                        "calibration_factor": 1.023,
                        "description": "Contador total - 1000 pulsos por litro"
                    },
                    "flow": {
                        "pulses_per_liter": 500,
                        "calibration_factor": 1.015,
                        "description": "Caudal instantáneo - 500 pulsos por litro"
                    }
                },
                "variables": ["total", "flow", "level", "temperature"],
                "provider_config": {
                    "api_key": "your_api_key",
                    "endpoint": "https://api.twin.com/data",
                    "timeout": 30
                },
                "alerts": {
                    "level_critical": 95.0,
                    "flow_minimum": 0.1,
                    "temperature_max": 30.0
                }
            }
        )
        print(f"✅ Punto de captación '{point.name}' creado")
        points = [point]
    
    # Configurar constantes de pulsos en puntos existentes
    for point in points:
        current_config = point.config or {}
        
        # Agregar configuración de pulsos si no existe
        if 'pulse_constants' not in current_config:
            current_config['pulse_constants'] = {
                "total": {
                    "pulses_per_liter": 1000,
                    "calibration_factor": 1.023,
                    "description": "Contador total - 1000 pulsos por litro"
                },
                "flow": {
                    "pulses_per_liter": 500,
                    "calibration_factor": 1.015,
                    "description": "Caudal instantáneo - 500 pulsos por litro"
                }
            }
            
            # Agregar variables si no existen
            if 'variables' not in current_config:
                current_config['variables'] = ["total", "flow", "level", "temperature"]
            
            point.config = current_config
            point.save()
            print(f"✅ Configuración de pulsos agregada a '{point.name}'")
        else:
            print(f"ℹ️  Punto '{point.name}' ya tiene configuración de pulsos")
    
    return points


def test_pulse_conversion():
    """Probar la conversión de pulsos"""
    print("\n🧪 Probando conversión de pulsos...")
    
    # Obtener un punto de captación
    point = CatchmentPoint.objects.first()
    if not point:
        print("❌ No hay puntos de captación para probar")
        return
    
    # Crear procesador
    processor = TelemetryProcessor()
    
    # Datos de prueba
    test_data = {
        "device_id": point.device_id,
        "total": 1500,      # PULSOS
        "flow": 15.5,       # l/s
        "level": 2.3,       # metros
        "temperature": 18.5 # °C
    }
    
    print(f"📊 Datos de prueba:")
    print(f"   Total: {test_data['total']} pulsos")
    print(f"   Flow: {test_data['flow']} l/s")
    print(f"   Level: {test_data['level']} m")
    
    # Procesar datos
    try:
        result = processor.process_catchment_point_data(point, test_data)
        
        print(f"\n✅ Resultado del procesamiento:")
        print(f"   Total: {test_data['total']} pulsos → {result.total:.6f} m³")
        print(f"   Flow: {test_data['flow']} l/s → {result.flow:.3f} l/s")
        print(f"   Level: {test_data['level']} m → {result.level:.3f} m")
        
        if result.resets:
            print(f"\n🔄 Conversiones aplicadas:")
            for reset in result.resets:
                print(f"   - {reset}")
        
        if result.alerts:
            print(f"\n⚠️  Alertas generadas:")
            for alert in result.alerts:
                print(f"   - {alert}")
        
        # Verificar conversión
        expected_total = 1500 / (1000 * 1000) * 1.023  # Con factor de calibración
        if abs(result.total - expected_total) < 0.000001:
            print(f"\n✅ Conversión correcta: {result.total:.6f} m³")
        else:
            print(f"\n❌ Error en conversión: esperado {expected_total:.6f}, obtenido {result.total:.6f}")
    
    except Exception as e:
        print(f"❌ Error en procesamiento: {e}")


def show_configuration():
    """Mostrar configuración actual"""
    print("\n📋 Configuración actual:")
    
    # Variables
    print("\n🔧 Variables configuradas:")
    variables = Variable.objects.all()
    for var in variables:
        print(f"   {var.code}: {var.name} ({var.unit})")
        if var.processing_config:
            rules = var.processing_config.get('rules', [])
            for rule in rules:
                if rule.get('type') == 'pulse_conversion':
                    print(f"     - Conversión: {rule.get('pulses_per_liter', 'N/A')} pulsos/l")
    
    # Puntos de captación
    print("\n🏞️ Puntos de captación:")
    points = CatchmentPoint.objects.all()
    for point in points:
        print(f"   {point.name} ({point.code})")
        pulse_config = point.config.get('pulse_constants', {}) if point.config else {}
        for var_name, config in pulse_config.items():
            pulses_per_liter = config.get('pulses_per_liter', 'N/A')
            calibration = config.get('calibration_factor', 'N/A')
            print(f"     - {var_name}: {pulses_per_liter} pulsos/l, calibración: {calibration}")


def main():
    """Función principal"""
    print("🚀 Configurando conversión de pulsos en Stack VPS")
    print("=" * 50)
    
    try:
        # 1. Crear variables
        variables = create_variables()
        
        # 2. Configurar puntos de captación
        points = configure_catchment_points()
        
        # 3. Mostrar configuración
        show_configuration()
        
        # 4. Probar conversión
        test_pulse_conversion()
        
        print("\n" + "=" * 50)
        print("✅ Configuración completada exitosamente!")
        print("\n📚 Para usar la conversión:")
        print("1. Los datos llegan con 'total' en pulsos")
        print("2. El procesador convierte automáticamente a m³")
        print("3. La conversión usa la fórmula: pulsos / (pulses_per_liter × 1000)")
        print("4. Se aplica el factor de calibración si está configurado")
        
    except Exception as e:
        print(f"❌ Error en la configuración: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 