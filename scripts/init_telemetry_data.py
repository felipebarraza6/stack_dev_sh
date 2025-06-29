#!/usr/bin/env python3
"""
Script de inicialización de datos para el sistema de telemetría
Crea datos de prueba para desarrollo y testing
"""
import os
import sys
import django
import random
from datetime import datetime, timedelta
import pytz
from decimal import Decimal

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from api.apps.telemetry.models.measurements import Measurement, MeasurementBatch, MeasurementQuality
from api.apps.telemetry.models.points import CatchmentPoint
from api.apps.telemetry.models.schemes import Variable, Scheme
from api.apps.erp.projects.models import Project

User = get_user_model()

# Configuración de zona horaria
CHILE_TZ = pytz.timezone('America/Santiago')


class TelemetryDataInitializer:
    """Inicializador de datos de telemetría"""
    
    def __init__(self):
        self.created_data = {
            'schemes': [],
            'variables': [],
            'points': [],
            'measurements': [],
            'batches': [],
            'quality_metrics': []
        }
    
    def create_test_user(self):
        """Crear usuario de prueba si no existe"""
        try:
            user = User.objects.get(username='telemetry_test')
            print(f"✅ Usuario de prueba ya existe: {user.username}")
            return user
        except User.DoesNotExist:
            user = User.objects.create_user(
                username='telemetry_test',
                email='telemetry@test.com',
                password='testpass123',
                is_staff=True
            )
            print(f"✅ Usuario de prueba creado: {user.username}")
            return user
    
    def create_test_project(self):
        """Crear proyecto de prueba si no existe"""
        try:
            project = Project.objects.get(name='Proyecto Telemetría Test')
            print(f"✅ Proyecto de prueba ya existe: {project.name}")
            return project
        except Project.DoesNotExist:
            project = Project.objects.create(
                name='Proyecto Telemetría Test',
                description='Proyecto para testing del sistema de telemetría',
                owner=self.test_user
            )
            print(f"✅ Proyecto de prueba creado: {project.name}")
            return project
    
    def create_schemes(self):
        """Crear esquemas de telemetría"""
        schemes_data = [
            {
                'name': 'Esquema Hidrológico Básico',
                'description': 'Esquema para mediciones hidrológicas básicas'
            },
            {
                'name': 'Esquema Hidrológico Avanzado',
                'description': 'Esquema para mediciones hidrológicas avanzadas'
            },
            {
                'name': 'Esquema Meteorológico',
                'description': 'Esquema para mediciones meteorológicas'
            }
        ]
        
        for scheme_data in schemes_data:
            scheme, created = Scheme.objects.get_or_create(
                name=scheme_data['name'],
                defaults=scheme_data
            )
            if created:
                print(f"✅ Esquema creado: {scheme.name}")
            else:
                print(f"✅ Esquema ya existe: {scheme.name}")
            self.created_data['schemes'].append(scheme)
    
    def create_variables(self):
        """Crear variables de telemetría"""
        variables_data = [
            # Esquema Hidrológico Básico
            {
                'scheme': self.created_data['schemes'][0],
                'name': 'level',
                'label': 'Nivel de Agua',
                'variable_type': 'LEVEL',
                'provider': 'TWIN',
                'unit': 'm',
                'pulse_factor': 1000,
                'constant_addition': 0,
                'extra_attributes': {'min_value': 0, 'max_value': 10}
            },
            {
                'scheme': self.created_data['schemes'][0],
                'name': 'flow',
                'label': 'Caudal',
                'variable_type': 'FLOW',
                'provider': 'TWIN',
                'unit': 'l/s',
                'pulse_factor': 1,
                'constant_addition': 0,
                'extra_attributes': {'min_value': 0, 'max_value': 1000}
            },
            {
                'scheme': self.created_data['schemes'][0],
                'name': 'total',
                'label': 'Totalizador',
                'variable_type': 'TOTAL',
                'provider': 'TWIN',
                'unit': 'm³',
                'pulse_factor': 1,
                'constant_addition': 0,
                'extra_attributes': {'min_value': 0, 'max_value': 999999}
            },
            
            # Esquema Hidrológico Avanzado
            {
                'scheme': self.created_data['schemes'][1],
                'name': 'level_high_precision',
                'label': 'Nivel de Alta Precisión',
                'variable_type': 'LEVEL',
                'provider': 'NETTRA',
                'unit': 'mm',
                'pulse_factor': 10000,
                'constant_addition': 0,
                'extra_attributes': {'precision': 0.1, 'min_value': 0, 'max_value': 10000}
            },
            {
                'scheme': self.created_data['schemes'][1],
                'name': 'flow_velocity',
                'label': 'Velocidad de Flujo',
                'variable_type': 'VELOCITY',
                'provider': 'NETTRA',
                'unit': 'm/s',
                'pulse_factor': 1,
                'constant_addition': 0,
                'extra_attributes': {'min_value': 0, 'max_value': 5}
            },
            {
                'scheme': self.created_data['schemes'][1],
                'name': 'temperature',
                'label': 'Temperatura del Agua',
                'variable_type': 'TEMPERATURE',
                'provider': 'NETTRA',
                'unit': '°C',
                'pulse_factor': 1,
                'constant_addition': 0,
                'extra_attributes': {'min_value': -10, 'max_value': 40}
            },
            
            # Esquema Meteorológico
            {
                'scheme': self.created_data['schemes'][2],
                'name': 'rainfall',
                'label': 'Precipitación',
                'variable_type': 'RAINFALL',
                'provider': 'NOVUS',
                'unit': 'mm',
                'pulse_factor': 1,
                'constant_addition': 0,
                'extra_attributes': {'min_value': 0, 'max_value': 1000}
            },
            {
                'scheme': self.created_data['schemes'][2],
                'name': 'air_temperature',
                'label': 'Temperatura del Aire',
                'variable_type': 'TEMPERATURE',
                'provider': 'NOVUS',
                'unit': '°C',
                'pulse_factor': 1,
                'constant_addition': 0,
                'extra_attributes': {'min_value': -40, 'max_value': 60}
            },
            {
                'scheme': self.created_data['schemes'][2],
                'name': 'humidity',
                'label': 'Humedad Relativa',
                'variable_type': 'HUMIDITY',
                'provider': 'NOVUS',
                'unit': '%',
                'pulse_factor': 1,
                'constant_addition': 0,
                'extra_attributes': {'min_value': 0, 'max_value': 100}
            }
        ]
        
        for var_data in variables_data:
            variable, created = Variable.objects.get_or_create(
                scheme=var_data['scheme'],
                name=var_data['name'],
                defaults=var_data
            )
            if created:
                print(f"✅ Variable creada: {variable.name} ({variable.scheme.name})")
            else:
                print(f"✅ Variable ya existe: {variable.name} ({variable.scheme.name})")
            self.created_data['variables'].append(variable)
    
    def create_points(self):
        """Crear puntos de captación"""
        points_data = [
            {
                'name': 'Estación Río Maipo',
                'project': self.test_project,
                'owner': self.test_user,
                'latitude': -33.4489,
                'longitude': -70.6693,
                'location': 'Río Maipo, Región Metropolitana',
                'frequency': '60',
                'is_telemetry_active': True,
                'telemetry_start_date': timezone.now().date(),
                'extra_attributes': {
                    'altitude': 500,
                    'basin': 'Maipo',
                    'station_type': 'river'
                }
            },
            {
                'name': 'Estación Embalse El Yeso',
                'project': self.test_project,
                'owner': self.test_user,
                'latitude': -33.6500,
                'longitude': -70.1000,
                'location': 'Embalse El Yeso, Cordillera de los Andes',
                'frequency': '60',
                'is_telemetry_active': True,
                'telemetry_start_date': timezone.now().date(),
                'extra_attributes': {
                    'altitude': 2500,
                    'basin': 'Maipo',
                    'station_type': 'reservoir'
                }
            },
            {
                'name': 'Estación Quebrada de Macul',
                'project': self.test_project,
                'owner': self.test_user,
                'latitude': -33.5000,
                'longitude': -70.5000,
                'location': 'Quebrada de Macul, Santiago',
                'frequency': '30',
                'is_telemetry_active': True,
                'telemetry_start_date': timezone.now().date(),
                'extra_attributes': {
                    'altitude': 800,
                    'basin': 'Maipo',
                    'station_type': 'stream'
                }
            },
            {
                'name': 'Estación Meteorológica Santiago',
                'project': self.test_project,
                'owner': self.test_user,
                'latitude': -33.4489,
                'longitude': -70.6693,
                'location': 'Santiago Centro',
                'frequency': '15',
                'is_telemetry_active': True,
                'telemetry_start_date': timezone.now().date(),
                'extra_attributes': {
                    'altitude': 520,
                    'station_type': 'weather',
                    'installation_date': '2020-01-01'
                }
            }
        ]
        
        for point_data in points_data:
            point, created = CatchmentPoint.objects.get_or_create(
                name=point_data['name'],
                project=point_data['project'],
                defaults=point_data
            )
            if created:
                print(f"✅ Punto creado: {point.name}")
            else:
                print(f"✅ Punto ya existe: {point.name}")
            self.created_data['points'].append(point)
    
    def assign_schemes_to_points(self):
        """Asignar esquemas a puntos"""
        # Asignar esquemas según el tipo de punto
        scheme_assignments = [
            (self.created_data['points'][0], [self.created_data['schemes'][0]]),  # Río Maipo - Básico
            (self.created_data['points'][1], [self.created_data['schemes'][0], self.created_data['schemes'][1]]),  # El Yeso - Básico + Avanzado
            (self.created_data['points'][2], [self.created_data['schemes'][0]]),  # Macul - Básico
            (self.created_data['points'][3], [self.created_data['schemes'][2]])   # Santiago - Meteorológico
        ]
        
        for point, schemes in scheme_assignments:
            for scheme in schemes:
                point.schemes.add(scheme)
            print(f"✅ Esquemas asignados a {point.name}: {[s.name for s in schemes]}")
    
    def generate_measurements(self, days_back=30):
        """Generar mediciones de prueba"""
        print(f"🔄 Generando mediciones para los últimos {days_back} días...")
        
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Configuraciones por variable
        variable_configs = {
            'level': {'min': 0.5, 'max': 3.0, 'trend': 0.1},
            'flow': {'min': 10, 'max': 200, 'trend': 5},
            'total': {'min': 1000, 'max': 50000, 'trend': 100},
            'level_high_precision': {'min': 500, 'max': 3000, 'trend': 10},
            'flow_velocity': {'min': 0.1, 'max': 2.0, 'trend': 0.05},
            'temperature': {'min': 8, 'max': 18, 'trend': 0.2},
            'rainfall': {'min': 0, 'max': 50, 'trend': 0},
            'air_temperature': {'min': 5, 'max': 25, 'trend': 0.3},
            'humidity': {'min': 30, 'max': 90, 'trend': 1}
        }
        
        measurements_to_create = []
        quality_metrics_to_create = []
        
        # Generar mediciones por punto y variable
        for point in self.created_data['points']:
            # Obtener variables disponibles para este punto
            available_variables = Variable.objects.filter(scheme__catchment_points=point)
            
            for variable in available_variables:
                config = variable_configs.get(variable.name, {'min': 0, 'max': 100, 'trend': 0})
                
                # Generar mediciones cada hora
                current_date = start_date
                base_value = random.uniform(config['min'], config['max'])
                
                while current_date <= end_date:
                    # Aplicar tendencia y variación
                    days_elapsed = (current_date - start_date).days
                    trend_value = base_value + (config['trend'] * days_elapsed)
                    noise = random.uniform(-0.1, 0.1) * (config['max'] - config['min'])
                    final_value = max(config['min'], min(config['max'], trend_value + noise))
                    
                    # Determinar tipo de valor
                    if variable.variable_type in ['TEMPERATURE', 'HUMIDITY', 'RAINFALL']:
                        value_numeric = Decimal(str(round(final_value, 2)))
                        value_text = None
                        value_boolean = None
                    elif variable.variable_type == 'TOTAL':
                        value_numeric = Decimal(str(int(final_value)))
                        value_text = None
                        value_boolean = None
                    else:
                        value_numeric = Decimal(str(round(final_value, 3)))
                        value_text = None
                        value_boolean = None
                    
                    # Calcular calidad (simular variaciones)
                    quality_score = random.uniform(0.7, 1.0)
                    if random.random() < 0.05:  # 5% de mediciones de baja calidad
                        quality_score = random.uniform(0.1, 0.6)
                    
                    # Crear medición
                    measurement = Measurement(
                        point=point,
                        variable=variable,
                        timestamp=current_date,
                        value_numeric=value_numeric,
                        value_text=value_text,
                        value_boolean=value_boolean,
                        raw_value={
                            'original_value': float(value_numeric),
                            'provider_data': {
                                'signal_strength': random.uniform(0.5, 1.0),
                                'battery_level': random.uniform(0.3, 1.0)
                            }
                        },
                        quality_score=quality_score,
                        provider=variable.provider,
                        processing_config={
                            'pulse_factor': variable.pulse_factor,
                            'unit_conversion': variable.unit,
                            'applied_filters': ['outlier_detection', 'smoothing']
                        },
                        days_since_last_connection=random.randint(0, 7)
                    )
                    measurements_to_create.append(measurement)
                    
                    # Crear métricas de calidad
                    quality_metric = MeasurementQuality(
                        measurement=measurement,
                        outlier_score=1.0 - quality_score,
                        consistency_score=random.uniform(0.8, 1.0),
                        completeness_score=random.uniform(0.9, 1.0),
                        is_outlier=quality_score < 0.5,
                        is_missing=False,
                        is_interpolated=False,
                        quality_notes=f"Generated test data - Quality: {quality_score:.2f}"
                    )
                    quality_metrics_to_create.append(quality_metric)
                    
                    current_date += timedelta(hours=1)
        
        # Bulk create measurements
        print(f"📊 Creando {len(measurements_to_create)} mediciones...")
        Measurement.objects.bulk_create(measurements_to_create, batch_size=1000)
        self.created_data['measurements'] = measurements_to_create
        
        # Bulk create quality metrics
        print(f"📊 Creando {len(quality_metrics_to_create)} métricas de calidad...")
        MeasurementQuality.objects.bulk_create(quality_metrics_to_create, batch_size=1000)
        self.created_data['quality_metrics'] = quality_metrics_to_create
    
    def create_test_batches(self):
        """Crear lotes de prueba"""
        print("🔄 Creando lotes de prueba...")
        
        batch_data = [
            {
                'batch_id': 'test_batch_001',
                'provider': 'TWIN',
                'frequency': '60',
                'total_measurements': 1000,
                'processed_measurements': 995,
                'failed_measurements': 5,
                'processing_time_ms': 1500,
                'status': 'completed',
                'metadata': {'test': True, 'source': 'script'}
            },
            {
                'batch_id': 'test_batch_002',
                'provider': 'NETTRA',
                'frequency': '60',
                'total_measurements': 800,
                'processed_measurements': 800,
                'failed_measurements': 0,
                'processing_time_ms': 1200,
                'status': 'completed',
                'metadata': {'test': True, 'source': 'script'}
            },
            {
                'batch_id': 'test_batch_003',
                'provider': 'NOVUS',
                'frequency': '15',
                'total_measurements': 2000,
                'processed_measurements': 1980,
                'failed_measurements': 20,
                'processing_time_ms': 2000,
                'status': 'completed',
                'metadata': {'test': True, 'source': 'script'}
            }
        ]
        
        for batch_info in batch_data:
            batch, created = MeasurementBatch.objects.get_or_create(
                batch_id=batch_info['batch_id'],
                defaults=batch_info
            )
            if created:
                print(f"✅ Lote creado: {batch.batch_id}")
            else:
                print(f"✅ Lote ya existe: {batch.batch_id}")
            self.created_data['batches'].append(batch)
    
    def run_initialization(self, generate_measurements=True, days_back=30):
        """Ejecutar inicialización completa"""
        print("🚀 Iniciando inicialización de datos de telemetría...")
        print("=" * 60)
        
        # Crear datos básicos
        self.test_user = self.create_test_user()
        self.test_project = self.create_test_project()
        
        print("\n📋 Creando esquemas...")
        self.create_schemes()
        
        print("\n📋 Creando variables...")
        self.create_variables()
        
        print("\n📋 Creando puntos de captación...")
        self.create_points()
        
        print("\n📋 Asignando esquemas a puntos...")
        self.assign_schemes_to_points()
        
        if generate_measurements:
            print("\n📋 Generando mediciones...")
            self.generate_measurements(days_back)
        
        print("\n📋 Creando lotes de prueba...")
        self.create_test_batches()
        
        # Generar reporte
        self.generate_report()
    
    def generate_report(self):
        """Generar reporte de inicialización"""
        print("\n" + "=" * 60)
        print("📊 REPORTE DE INICIALIZACIÓN")
        print("=" * 60)
        
        print(f"👤 Usuario de prueba: {self.test_user.username}")
        print(f"📁 Proyecto: {self.test_project.name}")
        print(f"📋 Esquemas creados: {len(self.created_data['schemes'])}")
        print(f"🔧 Variables creadas: {len(self.created_data['variables'])}")
        print(f"📍 Puntos creados: {len(self.created_data['points'])}")
        print(f"📊 Mediciones creadas: {len(self.created_data['measurements'])}")
        print(f"📈 Métricas de calidad: {len(self.created_data['quality_metrics'])}")
        print(f"📦 Lotes creados: {len(self.created_data['batches'])}")
        
        # Estadísticas por proveedor
        if self.created_data['measurements']:
            providers = {}
            for measurement in self.created_data['measurements']:
                provider = measurement.provider
                providers[provider] = providers.get(provider, 0) + 1
            
            print(f"\n📊 Mediciones por proveedor:")
            for provider, count in providers.items():
                print(f"   {provider}: {count}")
        
        # Estadísticas por variable
        if self.created_data['measurements']:
            variables = {}
            for measurement in self.created_data['measurements']:
                var_name = measurement.variable.name
                variables[var_name] = variables.get(var_name, 0) + 1
            
            print(f"\n📊 Mediciones por variable:")
            for var_name, count in variables.items():
                print(f"   {var_name}: {count}")
        
        print(f"\n✅ Inicialización completada exitosamente!")
        print(f"🎯 El sistema está listo para testing y desarrollo")
        print("=" * 60)


def main():
    """Función principal"""
    initializer = TelemetryDataInitializer()
    
    # Configurar parámetros
    import argparse
    parser = argparse.ArgumentParser(description='Inicializar datos de telemetría')
    parser.add_argument('--no-measurements', action='store_true', 
                       help='No generar mediciones (solo datos básicos)')
    parser.add_argument('--days', type=int, default=30,
                       help='Días hacia atrás para generar mediciones (default: 30)')
    
    args = parser.parse_args()
    
    # Ejecutar inicialización
    initializer.run_initialization(
        generate_measurements=not args.no_measurements,
        days_back=args.days
    )


if __name__ == "__main__":
    main() 