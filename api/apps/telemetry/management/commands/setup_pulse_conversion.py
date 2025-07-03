"""
Comando de gestión Django para configurar la conversión de pulsos
Uso: python manage.py setup_pulse_conversion
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.apps.variables.models import Variable
from api.apps.catchment.models import CatchmentPoint
from api.apps.telemetry.processors.processor import TelemetryProcessor

User = get_user_model()


class Command(BaseCommand):
    help = 'Configurar conversión de pulsos en el sistema'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            action='store_true',
            help='Ejecutar prueba de conversión después de la configuración',
        )
        parser.add_argument(
            '--show-config',
            action='store_true',
            help='Mostrar configuración actual',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Configurando conversión de pulsos en Stack VPS')
        )
        
        try:
            # 1. Crear variables
            self.create_variables()
            
            # 2. Configurar puntos de captación
            self.configure_catchment_points()
            
            # 3. Mostrar configuración si se solicita
            if options['show_config']:
                self.show_configuration()
            
            # 4. Probar conversión si se solicita
            if options['test']:
                self.test_pulse_conversion()
            
            self.stdout.write(
                self.style.SUCCESS('\n✅ Configuración completada exitosamente!')
            )
            
            self.stdout.write('\n📚 Para usar la conversión:')
            self.stdout.write('1. Los datos llegan con "total" en pulsos')
            self.stdout.write('2. El procesador convierte automáticamente a m³')
            self.stdout.write('3. La conversión usa la fórmula: pulsos / (pulses_per_liter × 1000)')
            self.stdout.write('4. Se aplica el factor de calibración si está configurado')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error en la configuración: {e}')
            )

    def create_variables(self):
        """Crear variables con configuración de procesamiento"""
        self.stdout.write('🔧 Creando variables...')
        
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
            self.stdout.write(self.style.SUCCESS('✅ Variable "total" creada'))
        else:
            self.stdout.write('ℹ️  Variable "total" ya existe')
        
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
            self.stdout.write(self.style.SUCCESS('✅ Variable "flow" creada'))
        else:
            self.stdout.write('ℹ️  Variable "flow" ya existe')

    def configure_catchment_points(self):
        """Configurar puntos de captación con constantes de pulsos"""
        self.stdout.write('\n🏞️ Configurando puntos de captación...')
        
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
                self.stdout.write(self.style.SUCCESS('✅ Usuario admin creado'))
        except Exception as e:
            self.stdout.write(f'⚠️  Error con usuario: {e}')
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
            self.stdout.write(self.style.SUCCESS(f'✅ Punto de captación "{point.name}" creado'))
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
                self.stdout.write(self.style.SUCCESS(f'✅ Configuración de pulsos agregada a "{point.name}"'))
            else:
                self.stdout.write(f'ℹ️  Punto "{point.name}" ya tiene configuración de pulsos')

    def test_pulse_conversion(self):
        """Probar la conversión de pulsos"""
        self.stdout.write('\n🧪 Probando conversión de pulsos...')
        
        # Obtener un punto de captación
        point = CatchmentPoint.objects.first()
        if not point:
            self.stdout.write(self.style.ERROR('❌ No hay puntos de captación para probar'))
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
        
        self.stdout.write('📊 Datos de prueba:')
        self.stdout.write(f'   Total: {test_data["total"]} pulsos')
        self.stdout.write(f'   Flow: {test_data["flow"]} l/s')
        self.stdout.write(f'   Level: {test_data["level"]} m')
        
        # Procesar datos
        try:
            result = processor.process_catchment_point_data(point, test_data)
            
            self.stdout.write('\n✅ Resultado del procesamiento:')
            self.stdout.write(f'   Total: {test_data["total"]} pulsos → {result.total:.6f} m³')
            self.stdout.write(f'   Flow: {test_data["flow"]} l/s → {result.flow:.3f} l/s')
            self.stdout.write(f'   Level: {test_data["level"]} m → {result.level:.3f} m')
            
            if result.resets:
                self.stdout.write('\n🔄 Conversiones aplicadas:')
                for reset in result.resets:
                    self.stdout.write(f'   - {reset}')
            
            if result.alerts:
                self.stdout.write('\n⚠️  Alertas generadas:')
                for alert in result.alerts:
                    self.stdout.write(f'   - {alert}')
            
            # Verificar conversión
            expected_total = 1500 / (1000 * 1000) * 1.023  # Con factor de calibración
            if abs(result.total - expected_total) < 0.000001:
                self.stdout.write(self.style.SUCCESS(f'\n✅ Conversión correcta: {result.total:.6f} m³'))
            else:
                self.stdout.write(self.style.ERROR(f'\n❌ Error en conversión: esperado {expected_total:.6f}, obtenido {result.total:.6f}'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error en procesamiento: {e}'))

    def show_configuration(self):
        """Mostrar configuración actual"""
        self.stdout.write('\n📋 Configuración actual:')
        
        # Variables
        self.stdout.write('\n🔧 Variables configuradas:')
        variables = Variable.objects.all()
        for var in variables:
            self.stdout.write(f'   {var.code}: {var.name} ({var.unit})')
            if var.processing_config:
                rules = var.processing_config.get('rules', [])
                for rule in rules:
                    if rule.get('type') == 'pulse_conversion':
                        self.stdout.write(f'     - Conversión: {rule.get("pulses_per_liter", "N/A")} pulsos/l')
        
        # Puntos de captación
        self.stdout.write('\n🏞️ Puntos de captación:')
        points = CatchmentPoint.objects.all()
        for point in points:
            self.stdout.write(f'   {point.name} ({point.code})')
            pulse_config = point.config.get('pulse_constants', {}) if point.config else {}
            for var_name, config in pulse_config.items():
                pulses_per_liter = config.get('pulses_per_liter', 'N/A')
                calibration = config.get('calibration_factor', 'N/A')
                self.stdout.write(f'     - {var_name}: {pulses_per_liter} pulsos/l, calibración: {calibration}') 