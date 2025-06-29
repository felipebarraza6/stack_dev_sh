#!/usr/bin/env python3
"""
Script de testing para el sistema completo de telemetría
Prueba el flujo completo desde recolección hasta almacenamiento
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

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings.development')
django.setup()

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de zona horaria
CHILE_TZ = pytz.timezone('America/Santiago')

# URLs de los servicios
TELEMETRY_COLLECTOR_URL = "http://localhost:8001"
DATA_PROCESSOR_URL = "http://localhost:8003"
DJANGO_API_URL = "http://localhost:8000"


class TelemetrySystemTester:
    """Tester para el sistema completo de telemetría"""
    
    def __init__(self):
        self.http_client = httpx.AsyncClient(timeout=30.0)
        self.test_results = {}
    
    async def test_telemetry_collector(self):
        """Probar el microservicio de telemetría"""
        logger.info("🧪 Probando Telemetry Collector...")
        
        try:
            # Health check
            response = await self.http_client.get(f"{TELEMETRY_COLLECTOR_URL}/health")
            if response.status_code == 200:
                logger.info("✅ Telemetry Collector - Health check OK")
                self.test_results['telemetry_collector_health'] = True
            else:
                logger.error(f"❌ Telemetry Collector - Health check failed: {response.status_code}")
                self.test_results['telemetry_collector_health'] = False
                return False
            
            # Stats
            response = await self.http_client.get(f"{TELEMETRY_COLLECTOR_URL}/stats")
            if response.status_code == 200:
                stats = response.json()
                logger.info(f"✅ Telemetry Collector - Stats: {stats}")
                self.test_results['telemetry_collector_stats'] = stats
            else:
                logger.error(f"❌ Telemetry Collector - Stats failed: {response.status_code}")
                self.test_results['telemetry_collector_stats'] = None
            
            # Test collection
            response = await self.http_client.post(f"{TELEMETRY_COLLECTOR_URL}/collect/frequency/60")
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Telemetry Collector - Collection started: {result}")
                self.test_results['telemetry_collector_collection'] = True
            else:
                logger.error(f"❌ Telemetry Collector - Collection failed: {response.status_code}")
                self.test_results['telemetry_collector_collection'] = False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Telemetry Collector test failed: {e}")
            self.test_results['telemetry_collector_error'] = str(e)
            return False
    
    async def test_data_processor(self):
        """Probar el microservicio de procesamiento de datos"""
        logger.info("🧪 Probando Data Processor...")
        
        try:
            # Health check
            response = await self.http_client.get(f"{DATA_PROCESSOR_URL}/health")
            if response.status_code == 200:
                logger.info("✅ Data Processor - Health check OK")
                self.test_results['data_processor_health'] = True
            else:
                logger.error(f"❌ Data Processor - Health check failed: {response.status_code}")
                self.test_results['data_processor_health'] = False
                return False
            
            # Stats
            response = await self.http_client.get(f"{DATA_PROCESSOR_URL}/stats")
            if response.status_code == 200:
                stats = response.json()
                logger.info(f"✅ Data Processor - Stats: {stats}")
                self.test_results['data_processor_stats'] = stats
            else:
                logger.error(f"❌ Data Processor - Stats failed: {response.status_code}")
                self.test_results['data_processor_stats'] = None
            
            # Test batch processing
            test_batch = {
                "batch_id": f"test_batch_{int(time.time())}",
                "provider": "twin",
                "frequency": "60",
                "measurements": [
                    {
                        "point_id": 1,
                        "variable_name": "level",
                        "timestamp": datetime.now(CHILE_TZ).isoformat(),
                        "value": 12.34,
                        "raw_value": {"original_value": 12.34, "provider_data": {}},
                        "provider": "twin",
                        "quality_score": 0.95,
                        "processing_config": {},
                        "days_since_last_connection": 0
                    }
                ],
                "metadata": {"test": True}
            }
            
            response = await self.http_client.post(
                f"{DATA_PROCESSOR_URL}/process/batch",
                json=test_batch
            )
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Data Processor - Batch processing started: {result}")
                self.test_results['data_processor_batch'] = True
            else:
                logger.error(f"❌ Data Processor - Batch processing failed: {response.status_code}")
                self.test_results['data_processor_batch'] = False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Data Processor test failed: {e}")
            self.test_results['data_processor_error'] = str(e)
            return False
    
    async def test_django_api(self):
        """Probar la API de Django"""
        logger.info("🧪 Probando Django API...")
        
        try:
            # Health check
            response = await self.http_client.get(f"{DJANGO_API_URL}/health/")
            if response.status_code == 200:
                logger.info("✅ Django API - Health check OK")
                self.test_results['django_api_health'] = True
            else:
                logger.error(f"❌ Django API - Health check failed: {response.status_code}")
                self.test_results['django_api_health'] = False
                return False
            
            # Test measurements endpoint
            response = await self.http_client.get(f"{DJANGO_API_URL}/api/telemetry/measurements/")
            if response.status_code == 200:
                measurements = response.json()
                logger.info(f"✅ Django API - Measurements endpoint OK: {len(measurements)} measurements")
                self.test_results['django_api_measurements'] = len(measurements)
            else:
                logger.error(f"❌ Django API - Measurements endpoint failed: {response.status_code}")
                self.test_results['django_api_measurements'] = None
            
            # Test stats endpoint
            response = await self.http_client.get(f"{DJANGO_API_URL}/api/telemetry/measurements/stats/")
            if response.status_code == 200:
                stats = response.json()
                logger.info(f"✅ Django API - Stats endpoint OK: {stats}")
                self.test_results['django_api_stats'] = stats
            else:
                logger.error(f"❌ Django API - Stats endpoint failed: {response.status_code}")
                self.test_results['django_api_stats'] = None
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Django API test failed: {e}")
            self.test_results['django_api_error'] = str(e)
            return False
    
    async def test_integration_flow(self):
        """Probar el flujo completo de integración"""
        logger.info("🧪 Probando flujo completo de integración...")
        
        try:
            # 1. Iniciar recolección
            response = await self.http_client.post(f"{TELEMETRY_COLLECTOR_URL}/collect/frequency/60")
            if response.status_code != 200:
                logger.error("❌ No se pudo iniciar la recolección")
                return False
            
            # 2. Esperar un poco para que se procesen los datos
            logger.info("⏳ Esperando procesamiento de datos...")
            await asyncio.sleep(5)
            
            # 3. Verificar que los datos llegaron al data processor
            response = await self.http_client.get(f"{DATA_PROCESSOR_URL}/stats")
            if response.status_code == 200:
                stats = response.json()
                logger.info(f"✅ Data Processor stats después de recolección: {stats}")
                self.test_results['integration_flow_stats'] = stats
            else:
                logger.error("❌ No se pudieron obtener stats del data processor")
                return False
            
            # 4. Verificar que los datos están en Django
            response = await self.http_client.get(f"{DJANGO_API_URL}/api/telemetry/measurements/")
            if response.status_code == 200:
                measurements = response.json()
                logger.info(f"✅ Django API tiene {len(measurements)} mediciones")
                self.test_results['integration_flow_measurements'] = len(measurements)
            else:
                logger.error("❌ No se pudieron obtener mediciones de Django")
                return False
            
            logger.info("✅ Flujo de integración completado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"❌ Flujo de integración falló: {e}")
            self.test_results['integration_flow_error'] = str(e)
            return False
    
    async def run_all_tests(self):
        """Ejecutar todas las pruebas"""
        logger.info("🚀 Iniciando pruebas del sistema de telemetría...")
        
        start_time = time.time()
        
        # Ejecutar pruebas individuales
        tests = [
            ("Telemetry Collector", self.test_telemetry_collector),
            ("Data Processor", self.test_data_processor),
            ("Django API", self.test_django_api),
        ]
        
        for test_name, test_func in tests:
            logger.info(f"\n{'='*50}")
            logger.info(f"Ejecutando: {test_name}")
            logger.info(f"{'='*50}")
            
            success = await test_func()
            self.test_results[f"{test_name.lower().replace(' ', '_')}_success"] = success
            
            if not success:
                logger.warning(f"⚠️ {test_name} falló, pero continuando con las demás pruebas...")
        
        # Ejecutar prueba de integración
        logger.info(f"\n{'='*50}")
        logger.info("Ejecutando: Flujo de Integración")
        logger.info(f"{'='*50}")
        
        integration_success = await self.test_integration_flow()
        self.test_results['integration_flow_success'] = integration_success
        
        # Generar reporte
        end_time = time.time()
        duration = end_time - start_time
        
        self.generate_report(duration)
    
    def generate_report(self, duration):
        """Generar reporte de pruebas"""
        logger.info(f"\n{'='*60}")
        logger.info("📊 REPORTE DE PRUEBAS DEL SISTEMA DE TELEMETRÍA")
        logger.info(f"{'='*60}")
        
        # Resumen de resultados
        total_tests = 4
        passed_tests = sum([
            self.test_results.get('telemetry_collector_success', False),
            self.test_results.get('data_processor_success', False),
            self.test_results.get('django_api_success', False),
            self.test_results.get('integration_flow_success', False)
        ])
        
        logger.info(f"⏱️  Duración total: {duration:.2f} segundos")
        logger.info(f"📈 Pruebas pasadas: {passed_tests}/{total_tests}")
        logger.info(f"📉 Pruebas fallidas: {total_tests - passed_tests}/{total_tests}")
        
        # Detalles por componente
        logger.info(f"\n🔍 DETALLES POR COMPONENTE:")
        
        # Telemetry Collector
        collector_success = self.test_results.get('telemetry_collector_success', False)
        logger.info(f"🔄 Telemetry Collector: {'✅ PASÓ' if collector_success else '❌ FALLÓ'}")
        if not collector_success:
            error = self.test_results.get('telemetry_collector_error', 'Error desconocido')
            logger.info(f"   Error: {error}")
        
        # Data Processor
        processor_success = self.test_results.get('data_processor_success', False)
        logger.info(f"⚙️  Data Processor: {'✅ PASÓ' if processor_success else '❌ FALLÓ'}")
        if not processor_success:
            error = self.test_results.get('data_processor_error', 'Error desconocido')
            logger.info(f"   Error: {error}")
        
        # Django API
        django_success = self.test_results.get('django_api_success', False)
        logger.info(f"🐍 Django API: {'✅ PASÓ' if django_success else '❌ FALLÓ'}")
        if not django_success:
            error = self.test_results.get('django_api_error', 'Error desconocido')
            logger.info(f"   Error: {error}")
        
        # Integration Flow
        integration_success = self.test_results.get('integration_flow_success', False)
        logger.info(f"🔗 Flujo de Integración: {'✅ PASÓ' if integration_success else '❌ FALLÓ'}")
        if not integration_success:
            error = self.test_results.get('integration_flow_error', 'Error desconocido')
            logger.info(f"   Error: {error}")
        
        # Estadísticas
        logger.info(f"\n📊 ESTADÍSTICAS:")
        if self.test_results.get('django_api_stats'):
            stats = self.test_results['django_api_stats']
            logger.info(f"   Total de mediciones: {stats.get('total_measurements', 0)}")
            logger.info(f"   Mediciones hoy: {stats.get('measurements_today', 0)}")
            logger.info(f"   Por proveedor: {stats.get('by_provider', {})}")
        
        # Recomendaciones
        logger.info(f"\n💡 RECOMENDACIONES:")
        if passed_tests == total_tests:
            logger.info("   🎉 ¡Sistema funcionando correctamente!")
            logger.info("   ✅ Todos los componentes están operativos")
            logger.info("   🚀 Listo para producción")
        else:
            logger.info("   ⚠️  Hay problemas que resolver:")
            if not self.test_results.get('telemetry_collector_success'):
                logger.info("   - Verificar que el telemetry-collector esté ejecutándose")
            if not self.test_results.get('data_processor_success'):
                logger.info("   - Verificar que el data-processor esté ejecutándose")
            if not self.test_results.get('django_api_success'):
                logger.info("   - Verificar que Django esté ejecutándose")
            if not self.test_results.get('integration_flow_success'):
                logger.info("   - Verificar la conectividad entre servicios")
        
        # Guardar reporte en archivo
        report_file = f"telemetry_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now(CHILE_TZ).isoformat(),
                'duration_seconds': duration,
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'results': self.test_results
            }, f, indent=2)
        
        logger.info(f"\n📄 Reporte guardado en: {report_file}")
        logger.info(f"{'='*60}")
    
    async def cleanup(self):
        """Limpiar recursos"""
        await self.http_client.aclose()


async def main():
    """Función principal"""
    tester = TelemetrySystemTester()
    
    try:
        await tester.run_all_tests()
    finally:
        await tester.cleanup()


if __name__ == "__main__":
    asyncio.run(main()) 