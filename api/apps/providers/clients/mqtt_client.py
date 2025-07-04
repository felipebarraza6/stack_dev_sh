"""
Cliente MQTT Dinámico
Sistema que escucha MQTT y pregunta por tokens automáticamente
"""
import asyncio
import json
import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import paho.mqtt.client as mqtt
from django.conf import settings
from django.core.cache import cache
from django.db import models

logger = logging.getLogger(__name__)


class DynamicMQTTClient:
    """Cliente MQTT dinámico que maneja múltiples brokers y tokens"""
    
    def __init__(self):
        self.clients = {}  # {provider_id: mqtt_client}
        self.message_handlers = {}  # {provider_id: handler_function}
        self.connection_status = {}  # {provider_id: status}
        self.device_tokens = {}  # {device_id: token}
        
    async def initialize(self):
        """Inicializar todos los clientes MQTT activos"""
        try:
            # Importar modelos localmente para evitar AppRegistryNotReady
            from api.apps.providers.models.providers.provider import Provider
            
            # Obtener todos los proveedores MQTT activos
            mqtt_providers = Provider.objects.filter(
                provider_type='MQTT',
                is_active=True
            ).prefetch_related('mqtt_config')
            
            for provider in mqtt_providers:
                await self.setup_provider(provider)
                
            logger.info(f"Inicializados {len(self.clients)} clientes MQTT")
            
        except Exception as e:
            logger.error(f"Error inicializando clientes MQTT: {str(e)}")
    
    async def setup_provider(self, provider):
        """Configurar un proveedor MQTT específico"""
        try:
            if not hasattr(provider, 'mqtt_config'):
                logger.warning(f"Proveedor {provider.name} no tiene configuración MQTT")
                return
            
            mqtt_config = provider.mqtt_config
            
            # Crear cliente MQTT
            client = mqtt.Client(
                client_id=f"telemetry_{provider.id}_{datetime.now().timestamp()}",
                clean_session=True
            )
            
            # Configurar callbacks
            client.on_connect = lambda client, userdata, flags, rc: self.on_connect(provider.id, client, userdata, flags, rc)
            client.on_message = lambda client, userdata, msg: self.on_message(provider.id, client, userdata, msg)
            client.on_disconnect = lambda client, userdata, rc: self.on_disconnect(provider.id, client, userdata, rc)
            
            # Configurar autenticación si existe
            if mqtt_config.username and mqtt_config.password:
                client.username_pw_set(mqtt_config.username, mqtt_config.password)
            
            # Configurar TLS si está habilitado
            if mqtt_config.use_tls:
                client.tls_set()
            
            # Conectar al broker
            client.connect(
                mqtt_config.broker_host,
                mqtt_config.broker_port,
                keepalive=mqtt_config.keepalive
            )
            
            # Iniciar loop en background
            client.loop_start()
            
            # Guardar cliente
            self.clients[provider.id] = client
            self.connection_status[provider.id] = 'CONNECTING'
            
            logger.info(f"Cliente MQTT configurado para {provider.name}")
            
        except Exception as e:
            logger.error(f"Error configurando proveedor {provider.name}: {str(e)}")
            self.connection_status[provider.id] = 'ERROR'
    
    def on_connect(self, provider_id: int, client, userdata, flags, rc):
        """Callback cuando se conecta al broker"""
        try:
            if rc == 0:
                logger.info(f"Conectado al broker MQTT del proveedor {provider_id}")
                self.connection_status[provider_id] = 'ONLINE'
                
                # Suscribirse a topics
                self.subscribe_to_topics(provider_id, client)
                
                # Actualizar estado en base de datos
                self.update_provider_status(provider_id, 'ONLINE')
                
            else:
                logger.error(f"Error conectando al broker MQTT: {rc}")
                self.connection_status[provider_id] = 'ERROR'
                self.update_provider_status(provider_id, 'ERROR')
                
        except Exception as e:
            logger.error(f"Error en on_connect: {str(e)}")
    
    def on_disconnect(self, provider_id: int, client, userdata, rc):
        """Callback cuando se desconecta del broker"""
        try:
            logger.warning(f"Desconectado del broker MQTT del proveedor {provider_id}")
            self.connection_status[provider_id] = 'OFFLINE'
            self.update_provider_status(provider_id, 'OFFLINE')
            
        except Exception as e:
            logger.error(f"Error en on_disconnect: {str(e)}")
    
    def subscribe_to_topics(self, provider_id: int, client):
        """Suscribirse a los topics del proveedor"""
        try:
            # Importar modelos localmente
            from api.apps.providers.models.providers.provider import Provider
            
            provider = Provider.objects.get(id=provider_id)
            mqtt_config = provider.mqtt_config
            
            # Topic para escuchar todos los dispositivos
            topic_pattern = f"{mqtt_config.topic_prefix}#"
            
            client.subscribe(topic_pattern, qos=mqtt_config.qos_level)
            logger.info(f"Suscrito a topic: {topic_pattern}")
            
        except Exception as e:
            logger.error(f"Error suscribiéndose a topics: {str(e)}")
    
    def on_message(self, provider_id: int, client, userdata, msg):
        """Callback cuando llega un mensaje MQTT"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            
            logger.debug(f"Mensaje recibido en topic {topic}: {payload}")
            
            # Extraer device_id del topic
            device_id = self.extract_device_id(topic, provider_id)
            if not device_id:
                logger.warning(f"No se pudo extraer device_id del topic: {topic}")
                return
            
            # Verificar token del dispositivo
            if not self.verify_device_token(device_id, provider_id):
                logger.warning(f"Token no válido para dispositivo: {device_id}")
                return
            
            # Procesar mensaje
            asyncio.create_task(self.process_mqtt_message(provider_id, device_id, payload))
            
        except Exception as e:
            logger.error(f"Error procesando mensaje MQTT: {str(e)}")
    
    def extract_device_id(self, topic: str, provider_id: int) -> Optional[str]:
        """Extraer device_id del topic MQTT"""
        try:
            # Importar modelos localmente
            from api.apps.providers.models.providers.provider import Provider
            
            provider = Provider.objects.get(id=provider_id)
            mqtt_config = provider.mqtt_config
            
            # Remover prefijo del topic
            if topic.startswith(mqtt_config.topic_prefix):
                topic_without_prefix = topic[len(mqtt_config.topic_prefix):]
                
                # Extraer device_id (asumiendo formato: device_id/...)
                parts = topic_without_prefix.split('/')
                if parts:
                    return parts[0]
            
            return None
            
        except Exception as e:
            logger.error(f"Error extrayendo device_id: {str(e)}")
            return None
    
    def verify_device_token(self, device_id: str, provider_id: int) -> bool:
        """Verificar si el dispositivo tiene un token válido"""
        try:
            # Importar modelos localmente
            from api.apps.providers.models.tokens.device_token import DeviceToken
            
            # Buscar en caché primero
            cache_key = f"device_token_{device_id}_{provider_id}"
            cached_token = cache.get(cache_key)
            
            if cached_token:
                return True
            
            # Buscar en base de datos
            token_exists = DeviceToken.objects.filter(
                provider_id=provider_id,
                device_id=device_id,
                is_active=True
            ).exists()
            
            if token_exists:
                # Guardar en caché por 1 hora
                cache.set(cache_key, True, 3600)
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error verificando token: {str(e)}")
            return False
    
    async def process_mqtt_message(self, provider_id: int, device_id: str, payload: str):
        """Procesar mensaje MQTT recibido"""
        try:
            # Parsear JSON
            data = json.loads(payload)
            
            # Buscar esquema apropiado
            schema = await self.find_appropriate_schema(provider_id, data)
            if not schema:
                logger.warning(f"No se encontró esquema apropiado para dispositivo {device_id}")
                return
            
            # Transformar datos según el esquema
            transformed_data = await self.transform_data(data, schema, provider_id)
            
            # Guardar datos procesados
            await self.save_processed_data(provider_id, device_id, schema, transformed_data)
            
            # Log de ingesta exitosa
            await self.log_ingestion(provider_id, device_id, schema, 'SUCCESS', 1, 0)
            
        except json.JSONDecodeError:
            logger.error(f"Error parseando JSON del dispositivo {device_id}")
            await self.log_ingestion(provider_id, device_id, None, 'ERROR', 0, 1, "JSON inválido")
            
        except Exception as e:
            logger.error(f"Error procesando mensaje de {device_id}: {str(e)}")
            await self.log_ingestion(provider_id, device_id, None, 'ERROR', 0, 1, str(e))
    
    async def find_appropriate_schema(self, provider_id: int, data: Dict[str, Any]) -> Optional[Any]:
        """Encontrar el esquema apropiado para los datos"""
        try:
            # Importar modelos localmente
            from api.apps.providers.models.providers.provider import ProviderSchemaMapping
            from api.apps.providers.models.schemas.data_schema import DataSchema
            
            # Obtener mapeos activos del proveedor
            mappings = ProviderSchemaMapping.objects.filter(
                provider_id=provider_id,
                is_active=True
            ).select_related('schema').order_by('priority')
            
            for mapping in mappings:
                schema = mapping.schema
                
                # Verificar si el esquema soporta estos datos
                if self.schema_matches_data(schema, data):
                    return schema
            
            return None
            
        except Exception as e:
            logger.error(f"Error buscando esquema: {str(e)}")
            return None
    
    def schema_matches_data(self, schema: Any, data: Dict[str, Any]) -> bool:
        """Verificar si el esquema coincide con los datos"""
        try:
            # Verificar si los datos contienen las variables soportadas
            supported_vars = schema.supported_variables
            
            for var in supported_vars:
                if var not in data:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error verificando esquema: {str(e)}")
            return False
    
    async def transform_data(self, data: Dict[str, Any], schema: Any, provider_id: int) -> Dict[str, Any]:
        """Transformar datos según el esquema y configuración del proveedor"""
        try:
            # Importar modelos localmente
            from api.apps.providers.models.providers.provider import ProviderSchemaMapping
            
            # Obtener configuración de transformación
            mapping = ProviderSchemaMapping.objects.get(
                provider_id=provider_id,
                schema=schema
            )
            
            transformations = mapping.data_transformations
            transformed_data = data.copy()
            
            # Aplicar transformaciones
            for field, transformation in transformations.items():
                if field in transformed_data:
                    if transformation.get('type') == 'multiply':
                        factor = transformation.get('factor', 1)
                        transformed_data[field] = float(transformed_data[field]) * factor
                    
                    elif transformation.get('type') == 'add':
                        value = transformation.get('value', 0)
                        transformed_data[field] = float(transformed_data[field]) + value
                    
                    elif transformation.get('type') == 'convert':
                        # Conversiones específicas (ej: m3 a l/s)
                        pass
            
            return transformed_data
            
        except Exception as e:
            logger.error(f"Error transformando datos: {str(e)}")
            return data
    
    async def save_processed_data(self, provider_id: int, device_id: str, schema: Any, data: Dict[str, Any]):
        """Guardar datos procesados en la base de datos"""
        try:
            # Aquí integrarías con tu modelo de datos existente
            # Por ahora solo log
            logger.info(f"Datos guardados para dispositivo {device_id}: {data}")
            
        except Exception as e:
            logger.error(f"Error guardando datos: {str(e)}")
    
    async def log_ingestion(self, provider_id: int, device_id: str, schema: Optional[Any], 
                          status: str, processed: int, failed: int, error_message: Optional[str] = None):
        """Registrar log de ingesta"""
        try:
            # Importar modelos localmente
            from api.apps.providers.models.logs.mqtt.broker import DataIngestionLog
            
            DataIngestionLog.objects.create(
                provider_id=provider_id,
                device_id=device_id,
                schema=schema,
                status=status,
                records_processed=processed,
                records_failed=failed,
                error_message=error_message,
                completed_at=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error registrando log de ingesta: {str(e)}")
    
    def update_provider_status(self, provider_id: int, status: str):
        """Actualizar estado del proveedor en base de datos"""
        try:
            # Importar modelos localmente
            from api.apps.providers.models.providers.provider import Provider
            
            Provider.objects.filter(id=provider_id).update(
                connection_status=status,
                last_connection=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error actualizando estado del proveedor: {str(e)}")
    
    async def add_device_token(self, provider_id: int, device_id: str, token: str, token_type: str = 'API_KEY'):
        """Agregar token de dispositivo dinámicamente"""
        try:
            # Importar modelos localmente
            from api.apps.providers.models.tokens.device_token import DeviceToken
            
            # Crear o actualizar token
            device_token, created = DeviceToken.objects.update_or_create(
                provider_id=provider_id,
                device_id=device_id,
                defaults={
                    'token': token,
                    'token_type': token_type,
                    'is_active': True,
                    'last_used': datetime.now()
                }
            )
            
            # Actualizar caché
            cache_key = f"device_token_{device_id}_{provider_id}"
            cache.set(cache_key, True, 3600)
            
            logger.info(f"Token {'creado' if created else 'actualizado'} para dispositivo {device_id}")
            
        except Exception as e:
            logger.error(f"Error agregando token: {str(e)}")
    
    async def remove_device_token(self, provider_id: int, device_id: str):
        """Remover token de dispositivo"""
        try:
            # Importar modelos localmente
            from api.apps.providers.models.tokens.device_token import DeviceToken
            
            DeviceToken.objects.filter(
                provider_id=provider_id,
                device_id=device_id
            ).update(is_active=False)
            
            # Remover de caché
            cache_key = f"device_token_{device_id}_{provider_id}"
            cache.delete(cache_key)
            
            logger.info(f"Token removido para dispositivo {device_id}")
            
        except Exception as e:
            logger.error(f"Error removiendo token: {str(e)}")
    
    async def shutdown(self):
        """Cerrar todas las conexiones MQTT"""
        try:
            for provider_id, client in self.clients.items():
                client.loop_stop()
                client.disconnect()
                logger.info(f"Cliente MQTT desconectado para proveedor {provider_id}")
            
            self.clients.clear()
            self.connection_status.clear()
            
        except Exception as e:
            logger.error(f"Error cerrando clientes MQTT: {str(e)}")


# Instancia global del cliente MQTT
mqtt_client = DynamicMQTTClient() 