#!/usr/bin/env python3
"""
Script de monitoreo en tiempo real del sistema de telemetría
Monitorea el estado de todos los componentes y genera alertas
"""
import os
import sys
import django
import asyncio
import json
import time
from datetime import datetime, timedelta
import pytz
import httpx
import logging
from typing import Dict, List, Any
import psutil
import subprocess

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings.development')
django.setup()

from django.db import connection
from django.core.cache import cache
from api.apps.telemetry.models.measurements import Measurement, MeasurementBatch

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración de zona horaria
CHILE_TZ = pytz.timezone('America/Santiago')

# URLs de los servicios
SERVICES = {
    'telemetry_collector': 'http://localhost:8001',
    'data_processor': 'http://localhost:8003',
    'django_api': 'http://localhost:8000',
    'redis': 'localhost:6379',
    'postgres': 'localhost:5432'
}

# Umbrales de alerta
ALERT_THRESHOLDS = {
    'measurements_per_hour': 100,  # Mínimo de mediciones por hora
    'processing_time_ms': 5000,    # Máximo tiempo de procesamiento
    'error_rate': 0.05,            # Máximo 5% de errores
    'memory_usage': 0.8,           # Máximo 80% de uso de memoria
    'disk_usage': 0.9,             # Máximo 90% de uso de disco
    'response_time_ms': 2000       # Máximo tiempo de respuesta
}


class TelemetrySystemMonitor:
    """Monitor del sistema de telemetría"""
    
    def __init__(self):
        self.http_client = httpx.AsyncClient(timeout=10.0)
        self.monitoring_data = {}
        self.alerts = []
        self.start_time = time.time()
    
    async def check_service_health(self, service_name: str, url: str) -> Dict[str, Any]:
        """Verificar salud de un servicio"""
        try:
            start_time = time.time()
            response = await self.http_client.get(f"{url}/health")
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                health_data = response.json()
                return {
                    'status': 'healthy',
                    'response_time_ms': response_time,
                    'data': health_data,
                    'last_check': datetime.now(CHILE_TZ).isoformat()
                }
            else:
                return {
                    'status': 'unhealthy',
                    'response_time_ms': response_time,
                    'error': f"HTTP {response.status_code}",
                    'last_check': datetime.now(CHILE_TZ).isoformat()
                }
        except Exception as e:
            return {
                'status': 'unreachable',
                'response_time_ms': None,
                'error': str(e),
                'last_check': datetime.now(CHILE_TZ).isoformat()
            }
    
    async def check_telemetry_collector(self) -> Dict[str, Any]:
        """Verificar estado del telemetry collector"""
        logger.info("🔍 Verificando Telemetry Collector...")
        
        # Health check
        health = await self.check_service_health('telemetry_collector', SERVICES['telemetry_collector'])
        
        # Stats
        try:
            response = await self.http_client.get(f"{SERVICES['telemetry_collector']}/stats")
            if response.status_code == 200:
                stats = response.json()
            else:
                stats = None
        except Exception as e:
            stats = None
            logger.error(f"Error obteniendo stats del collector: {e}")
        
        return {
            'health': health,
            'stats': stats,
            'service': 'telemetry_collector'
        }
    
    async def check_data_processor(self) -> Dict[str, Any]:
        """Verificar estado del data processor"""
        logger.info("🔍 Verificando Data Processor...")
        
        # Health check
        health = await self.check_service_health('data_processor', SERVICES['data_processor'])
        
        # Stats
        try:
            response = await self.http_client.get(f"{SERVICES['data_processor']}/stats")
            if response.status_code == 200:
                stats = response.json()
            else:
                stats = None
        except Exception as e:
            stats = None
            logger.error(f"Error obteniendo stats del processor: {e}")
        
        return {
            'health': health,
            'stats': stats,
            'service': 'data_processor'
        }
    
    async def check_django_api(self) -> Dict[str, Any]:
        """Verificar estado de la API de Django"""
        logger.info("🔍 Verificando Django API...")
        
        # Health check
        health = await self.check_service_health('django_api', SERVICES['django_api'])
        
        # Stats de mediciones
        try:
            response = await self.http_client.get(f"{SERVICES['django_api']}/api/telemetry/measurements/stats/")
            if response.status_code == 200:
                stats = response.json()
            else:
                stats = None
        except Exception as e:
            stats = None
            logger.error(f"Error obteniendo stats de Django: {e}")
        
        return {
            'health': health,
            'stats': stats,
            'service': 'django_api'
        }
    
    def check_database_health(self) -> Dict[str, Any]:
        """Verificar salud de la base de datos"""
        logger.info("🔍 Verificando base de datos...")
        
        try:
            # Verificar conexión
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            
            # Estadísticas de la base de datos
            total_measurements = Measurement.objects.count()
            recent_measurements = Measurement.objects.filter(
                timestamp__gte=timezone.now() - timedelta(hours=1)
            ).count()
            
            # Verificar lotes recientes
            recent_batches = MeasurementBatch.objects.filter(
                created_at__gte=timezone.now() - timedelta(hours=1)
            )
            completed_batches = recent_batches.filter(status='completed').count()
            failed_batches = recent_batches.filter(status='failed').count()
            total_batches = recent_batches.count()
            
            error_rate = failed_batches / total_batches if total_batches > 0 else 0
            
            return {
                'status': 'healthy',
                'total_measurements': total_measurements,
                'recent_measurements': recent_measurements,
                'recent_batches': {
                    'total': total_batches,
                    'completed': completed_batches,
                    'failed': failed_batches,
                    'error_rate': error_rate
                },
                'last_check': datetime.now(CHILE_TZ).isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'last_check': datetime.now(CHILE_TZ).isoformat()
            }
    
    def check_redis_health(self) -> Dict[str, Any]:
        """Verificar salud de Redis"""
        logger.info("🔍 Verificando Redis...")
        
        try:
            # Verificar conexión a Redis
            cache.set('health_check', 'ok', 60)
            result = cache.get('health_check')
            
            if result == 'ok':
                return {
                    'status': 'healthy',
                    'last_check': datetime.now(CHILE_TZ).isoformat()
                }
            else:
                return {
                    'status': 'unhealthy',
                    'error': 'Cache test failed',
                    'last_check': datetime.now(CHILE_TZ).isoformat()
                }
                
        except Exception as e:
            return {
                'status': 'unreachable',
                'error': str(e),
                'last_check': datetime.now(CHILE_TZ).isoformat()
            }
    
    def check_system_resources(self) -> Dict[str, Any]:
        """Verificar recursos del sistema"""
        logger.info("🔍 Verificando recursos del sistema...")
        
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memoria
            memory = psutil.virtual_memory()
            memory_percent = memory.percent / 100
            
            # Disco
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent / 100
            
            # Red
            network = psutil.net_io_counters()
            
            return {
                'cpu': {
                    'usage_percent': cpu_percent,
                    'cores': psutil.cpu_count()
                },
                'memory': {
                    'total_gb': memory.total / (1024**3),
                    'used_gb': memory.used / (1024**3),
                    'usage_percent': memory_percent
                },
                'disk': {
                    'total_gb': disk.total / (1024**3),
                    'used_gb': disk.used / (1024**3),
                    'usage_percent': disk_percent
                },
                'network': {
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv
                },
                'last_check': datetime.now(CHILE_TZ).isoformat()
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'last_check': datetime.now(CHILE_TZ).isoformat()
            }
    
    def check_docker_containers(self) -> Dict[str, Any]:
        """Verificar estado de contenedores Docker"""
        logger.info("🔍 Verificando contenedores Docker...")
        
        try:
            result = subprocess.run(
                ['docker', 'ps', '--format', 'json'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                containers = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        try:
                            container = json.loads(line)
                            containers.append({
                                'name': container.get('Names', ''),
                                'status': container.get('Status', ''),
                                'ports': container.get('Ports', ''),
                                'image': container.get('Image', '')
                            })
                        except json.JSONDecodeError:
                            continue
                
                return {
                    'status': 'healthy',
                    'containers': containers,
                    'total_containers': len(containers),
                    'last_check': datetime.now(CHILE_TZ).isoformat()
                }
            else:
                return {
                    'status': 'error',
                    'error': result.stderr,
                    'last_check': datetime.now(CHILE_TZ).isoformat()
                }
                
        except Exception as e:
            return {
                'status': 'unreachable',
                'error': str(e),
                'last_check': datetime.now(CHILE_TZ).isoformat()
            }
    
    def generate_alerts(self) -> List[Dict[str, Any]]:
        """Generar alertas basadas en los datos de monitoreo"""
        alerts = []
        
        # Verificar servicios
        for service_name, service_data in self.monitoring_data.items():
            if 'health' in service_data:
                health = service_data['health']
                if health['status'] != 'healthy':
                    alerts.append({
                        'level': 'critical',
                        'service': service_name,
                        'message': f"Servicio {service_name} no está saludable: {health.get('error', 'Unknown error')}",
                        'timestamp': datetime.now(CHILE_TZ).isoformat()
                    })
                
                # Verificar tiempo de respuesta
                if health.get('response_time_ms') and health['response_time_ms'] > ALERT_THRESHOLDS['response_time_ms']:
                    alerts.append({
                        'level': 'warning',
                        'service': service_name,
                        'message': f"Tiempo de respuesta alto en {service_name}: {health['response_time_ms']:.0f}ms",
                        'timestamp': datetime.now(CHILE_TZ).isoformat()
                    })
        
        # Verificar base de datos
        if 'database' in self.monitoring_data:
            db_data = self.monitoring_data['database']
            if db_data['status'] != 'healthy':
                alerts.append({
                    'level': 'critical',
                    'service': 'database',
                    'message': f"Base de datos no está saludable: {db_data.get('error', 'Unknown error')}",
                    'timestamp': datetime.now(CHILE_TZ).isoformat()
                })
            
            # Verificar tasa de errores en lotes
            if 'recent_batches' in db_data:
                error_rate = db_data['recent_batches']['error_rate']
                if error_rate > ALERT_THRESHOLDS['error_rate']:
                    alerts.append({
                        'level': 'warning',
                        'service': 'database',
                        'message': f"Alta tasa de errores en lotes: {error_rate:.2%}",
                        'timestamp': datetime.now(CHILE_TZ).isoformat()
                    })
        
        # Verificar recursos del sistema
        if 'system' in self.monitoring_data:
            system_data = self.monitoring_data['system']
            
            if 'memory' in system_data:
                memory_usage = system_data['memory']['usage_percent']
                if memory_usage > ALERT_THRESHOLDS['memory_usage']:
                    alerts.append({
                        'level': 'warning',
                        'service': 'system',
                        'message': f"Alto uso de memoria: {memory_usage:.1%}",
                        'timestamp': datetime.now(CHILE_TZ).isoformat()
                    })
            
            if 'disk' in system_data:
                disk_usage = system_data['disk']['usage_percent']
                if disk_usage > ALERT_THRESHOLDS['disk_usage']:
                    alerts.append({
                        'level': 'critical',
                        'service': 'system',
                        'message': f"Alto uso de disco: {disk_usage:.1%}",
                        'timestamp': datetime.now(CHILE_TZ).isoformat()
                    })
        
        return alerts
    
    async def run_monitoring_cycle(self):
        """Ejecutar un ciclo completo de monitoreo"""
        logger.info("🔄 Iniciando ciclo de monitoreo...")
        
        # Verificar servicios
        self.monitoring_data['telemetry_collector'] = await self.check_telemetry_collector()
        self.monitoring_data['data_processor'] = await self.check_data_processor()
        self.monitoring_data['django_api'] = await self.check_django_api()
        
        # Verificar infraestructura
        self.monitoring_data['database'] = self.check_database_health()
        self.monitoring_data['redis'] = self.check_redis_health()
        self.monitoring_data['system'] = self.check_system_resources()
        self.monitoring_data['docker'] = self.check_docker_containers()
        
        # Generar alertas
        self.alerts = self.generate_alerts()
        
        # Mostrar resumen
        self.display_summary()
    
    def display_summary(self):
        """Mostrar resumen del monitoreo"""
        print("\n" + "=" * 80)
        print("📊 RESUMEN DE MONITOREO DEL SISTEMA DE TELEMETRÍA")
        print("=" * 80)
        
        # Estado general
        healthy_services = 0
        total_services = 0
        
        for service_name, service_data in self.monitoring_data.items():
            if 'health' in service_data:
                total_services += 1
                if service_data['health']['status'] == 'healthy':
                    healthy_services += 1
        
        print(f"🏥 Estado General: {healthy_services}/{total_services} servicios saludables")
        
        # Servicios
        print(f"\n🔧 SERVICIOS:")
        for service_name, service_data in self.monitoring_data.items():
            if 'health' in service_data:
                health = service_data['health']
                status_icon = "✅" if health['status'] == 'healthy' else "❌"
                response_time = f"({health['response_time_ms']:.0f}ms)" if health.get('response_time_ms') else ""
                print(f"   {status_icon} {service_name}: {health['status']} {response_time}")
        
        # Base de datos
        if 'database' in self.monitoring_data:
            db_data = self.monitoring_data['database']
            status_icon = "✅" if db_data['status'] == 'healthy' else "❌"
            print(f"\n🗄️  BASE DE DATOS:")
            print(f"   {status_icon} Estado: {db_data['status']}")
            if 'total_measurements' in db_data:
                print(f"   📊 Total mediciones: {db_data['total_measurements']:,}")
                print(f"   📈 Mediciones última hora: {db_data['recent_measurements']}")
        
        # Recursos del sistema
        if 'system' in self.monitoring_data:
            system_data = self.monitoring_data['system']
            print(f"\n💻 RECURSOS DEL SISTEMA:")
            if 'cpu' in system_data:
                print(f"   🖥️  CPU: {system_data['cpu']['usage_percent']:.1f}%")
            if 'memory' in system_data:
                memory = system_data['memory']
                print(f"   🧠 Memoria: {memory['usage_percent']:.1f}% ({memory['used_gb']:.1f}GB / {memory['total_gb']:.1f}GB)")
            if 'disk' in system_data:
                disk = system_data['disk']
                print(f"   💾 Disco: {disk['usage_percent']:.1f}% ({disk['used_gb']:.1f}GB / {disk['total_gb']:.1f}GB)")
        
        # Alertas
        if self.alerts:
            print(f"\n🚨 ALERTAS ({len(self.alerts)}):")
            for alert in self.alerts:
                level_icon = "🔴" if alert['level'] == 'critical' else "🟡"
                print(f"   {level_icon} [{alert['level'].upper()}] {alert['message']}")
        else:
            print(f"\n✅ No hay alertas activas")
        
        print("=" * 80)
    
    async def continuous_monitoring(self, interval_seconds=60):
        """Monitoreo continuo"""
        logger.info(f"🚀 Iniciando monitoreo continuo (intervalo: {interval_seconds}s)")
        
        try:
            while True:
                await self.run_monitoring_cycle()
                
                # Guardar datos de monitoreo
                self.save_monitoring_data()
                
                # Esperar hasta el siguiente ciclo
                await asyncio.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            logger.info("⏹️  Monitoreo detenido por el usuario")
        except Exception as e:
            logger.error(f"❌ Error en monitoreo continuo: {e}")
        finally:
            await self.cleanup()
    
    def save_monitoring_data(self):
        """Guardar datos de monitoreo"""
        try:
            timestamp = datetime.now(CHILE_TZ).isoformat()
            monitoring_file = f"monitoring_data_{datetime.now().strftime('%Y%m%d')}.json"
            
            data = {
                'timestamp': timestamp,
                'monitoring_data': self.monitoring_data,
                'alerts': self.alerts
            }
            
            # Guardar en archivo
            with open(monitoring_file, 'a') as f:
                f.write(json.dumps(data) + '\n')
            
            # Mantener solo las últimas 1000 líneas
            with open(monitoring_file, 'r') as f:
                lines = f.readlines()
            
            if len(lines) > 1000:
                with open(monitoring_file, 'w') as f:
                    f.writelines(lines[-1000:])
                    
        except Exception as e:
            logger.error(f"Error guardando datos de monitoreo: {e}")
    
    async def cleanup(self):
        """Limpiar recursos"""
        await self.http_client.aclose()


async def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor del sistema de telemetría')
    parser.add_argument('--interval', type=int, default=60,
                       help='Intervalo de monitoreo en segundos (default: 60)')
    parser.add_argument('--once', action='store_true',
                       help='Ejecutar solo una vez')
    
    args = parser.parse_args()
    
    monitor = TelemetrySystemMonitor()
    
    if args.once:
        await monitor.run_monitoring_cycle()
    else:
        await monitor.continuous_monitoring(args.interval)


if __name__ == "__main__":
    asyncio.run(main()) 