"""
Sistema de Proveedores Unificado
Maneja la comunicación con todos los proveedores de datos de telemetría
"""
import logging
import asyncio
import aiohttp
import requests
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from dataclasses import dataclass

from api.telemetry.config import telemetry_config, ProviderConfig

logger = logging.getLogger(__name__)


@dataclass
class ProviderData:
    """Datos obtenidos de un proveedor"""
    provider_name: str
    device_id: str
    timestamp: datetime
    data: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None


class BaseProvider(ABC):
    """Clase base para todos los proveedores"""
    
    def __init__(self, config: ProviderConfig):
        self.config = config
        self.session = None
    
    @abstractmethod
    async def fetch_data(self, device_id: str) -> ProviderData:
        """Obtener datos de un dispositivo específico"""
        pass
    
    @abstractmethod
    def parse_response(self, response: Any) -> Dict[str, Any]:
        """Parsear la respuesta del proveedor"""
        pass
    
    async def _make_request(self, url: str, method: str = 'GET', 
                          headers: Dict[str, str] = None, 
                          data: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Realizar petición HTTP con manejo de errores"""
        try:
            if not self.session:
                timeout = aiohttp.ClientTimeout(total=self.config.timeout)
                self.session = aiohttp.ClientSession(timeout=timeout)
            
            async with self.session.request(
                method=method,
                url=url,
                headers=headers,
                json=data
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Error HTTP {response.status} para {url}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error en petición a {url}: {str(e)}")
            return None


class TwinProvider(BaseProvider):
    """Proveedor Twin"""
    
    async def fetch_data(self, device_id: str) -> ProviderData:
        """Obtener datos del proveedor Twin"""
        try:
            url = f"{self.config.api_endpoint}/device/{device_id}/data"
            headers = {
                'Authorization': f"Bearer {self.config.authentication['api_key']}",
                'Content-Type': 'application/json'
            }
            
            response_data = await self._make_request(url, headers=headers)
            
            if response_data:
                parsed_data = self.parse_response(response_data)
                return ProviderData(
                    provider_name=self.config.name,
                    device_id=device_id,
                    timestamp=datetime.now(),
                    data=parsed_data,
                    success=True
                )
            else:
                return ProviderData(
                    provider_name=self.config.name,
                    device_id=device_id,
                    timestamp=datetime.now(),
                    data={},
                    success=False,
                    error_message="No se pudo obtener respuesta del servidor"
                )
                
        except Exception as e:
            logger.error(f"Error obteniendo datos de Twin para {device_id}: {str(e)}")
            return ProviderData(
                provider_name=self.config.name,
                device_id=device_id,
                timestamp=datetime.now(),
                data={},
                success=False,
                error_message=str(e)
            )
    
    def parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parsear respuesta específica de Twin"""
        try:
            return {
                'flow': float(response.get('flow', 0.0)),
                'total': float(response.get('total', 0.0)),
                'level': float(response.get('level', 0.0)),
                'pulses': int(response.get('pulses', 0)),
                'timestamp': response.get('timestamp', datetime.now().isoformat()),
                'device_id': response.get('device_id', ''),
                'send_dga': response.get('send_dga', False),
                'total_diff': response.get('total_diff', 0),
                'total_today_diff': response.get('total_today_diff', 0)
            }
        except Exception as e:
            logger.error(f"Error parseando respuesta de Twin: {str(e)}")
            return {}


class NettraProvider(BaseProvider):
    """Proveedor Nettra"""
    
    async def fetch_data(self, device_id: str) -> ProviderData:
        """Obtener datos del proveedor Nettra"""
        try:
            url = f"{self.config.api_endpoint}/api/v1/device/{device_id}"
            auth = aiohttp.BasicAuth(
                self.config.authentication['username'],
                self.config.authentication['password']
            )
            
            response_data = await self._make_request(url, auth=auth)
            
            if response_data:
                parsed_data = self.parse_response(response_data)
                return ProviderData(
                    provider_name=self.config.name,
                    device_id=device_id,
                    timestamp=datetime.now(),
                    data=parsed_data,
                    success=True
                )
            else:
                return ProviderData(
                    provider_name=self.config.name,
                    device_id=device_id,
                    timestamp=datetime.now(),
                    data={},
                    success=False,
                    error_message="No se pudo obtener respuesta del servidor"
                )
                
        except Exception as e:
            logger.error(f"Error obteniendo datos de Nettra para {device_id}: {str(e)}")
            return ProviderData(
                provider_name=self.config.name,
                device_id=device_id,
                timestamp=datetime.now(),
                data={},
                success=False,
                error_message=str(e)
            )
    
    def parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parsear respuesta específica de Nettra"""
        try:
            return {
                'flow': float(response.get('caudal', 0.0)),
                'total': float(response.get('acumulado', 0.0)),
                'level': float(response.get('nivel', 0.0)),
                'pulses': int(response.get('pulsos', 0)),
                'timestamp': response.get('fecha_medicion', datetime.now().isoformat()),
                'device_id': response.get('id_dispositivo', ''),
                'send_dga': response.get('enviar_dga', False),
                'total_diff': response.get('diferencia_total', 0),
                'total_today_diff': response.get('diferencia_hoy', 0)
            }
        except Exception as e:
            logger.error(f"Error parseando respuesta de Nettra: {str(e)}")
            return {}


class NovusProvider(BaseProvider):
    """Proveedor Novus"""
    
    async def fetch_data(self, device_id: str) -> ProviderData:
        """Obtener datos del proveedor Novus"""
        try:
            url = f"{self.config.api_endpoint}/devices/{device_id}/telemetry"
            headers = {
                'Authorization': f"Token {self.config.authentication['token']}",
                'Content-Type': 'application/json'
            }
            
            response_data = await self._make_request(url, headers=headers)
            
            if response_data:
                parsed_data = self.parse_response(response_data)
                return ProviderData(
                    provider_name=self.config.name,
                    device_id=device_id,
                    timestamp=datetime.now(),
                    data=parsed_data,
                    success=True
                )
            else:
                return ProviderData(
                    provider_name=self.config.name,
                    device_id=device_id,
                    timestamp=datetime.now(),
                    data={},
                    success=False,
                    error_message="No se pudo obtener respuesta del servidor"
                )
                
        except Exception as e:
            logger.error(f"Error obteniendo datos de Novus para {device_id}: {str(e)}")
            return ProviderData(
                provider_name=self.config.name,
                device_id=device_id,
                timestamp=datetime.now(),
                data={},
                success=False,
                error_message=str(e)
            )
    
    def parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parsear respuesta específica de Novus"""
        try:
            return {
                'flow': float(response.get('flow_rate', 0.0)),
                'total': float(response.get('total_volume', 0.0)),
                'level': float(response.get('water_level', 0.0)),
                'pulses': int(response.get('pulse_count', 0)),
                'timestamp': response.get('measurement_time', datetime.now().isoformat()),
                'device_id': response.get('device_identifier', ''),
                'send_dga': response.get('send_to_dga', False),
                'total_diff': response.get('volume_diff', 0),
                'total_today_diff': response.get('today_volume', 0)
            }
        except Exception as e:
            logger.error(f"Error parseando respuesta de Novus: {str(e)}")
            return {}


class TagoProvider(BaseProvider):
    """Proveedor Tago"""
    
    async def fetch_data(self, device_id: str) -> ProviderData:
        """Obtener datos del proveedor Tago"""
        try:
            url = f"{self.config.api_endpoint}/data"
            headers = {
                'Device-Token': self.config.authentication['device_token'],
                'Content-Type': 'application/json'
            }
            
            response_data = await self._make_request(url, headers=headers)
            
            if response_data:
                parsed_data = self.parse_response(response_data)
                return ProviderData(
                    provider_name=self.config.name,
                    device_id=device_id,
                    timestamp=datetime.now(),
                    data=parsed_data,
                    success=True
                )
            else:
                return ProviderData(
                    provider_name=self.config.name,
                    device_id=device_id,
                    timestamp=datetime.now(),
                    data={},
                    success=False,
                    error_message="No se pudo obtener respuesta del servidor"
                )
                
        except Exception as e:
            logger.error(f"Error obteniendo datos de Tago para {device_id}: {str(e)}")
            return ProviderData(
                provider_name=self.config.name,
                device_id=device_id,
                timestamp=datetime.now(),
                data={},
                success=False,
                error_message=str(e)
            )
    
    def parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parsear respuesta específica de Tago"""
        try:
            # Tago devuelve un array de variables
            variables = response.get('result', [])
            data = {
                'flow': 0.0,
                'total': 0.0,
                'level': 0.0,
                'pulses': 0,
                'timestamp': datetime.now().isoformat(),
                'device_id': '',
                'send_dga': False,
                'total_diff': 0,
                'total_today_diff': 0
            }
            
            for var in variables:
                variable_name = var.get('variable', '')
                value = var.get('value', 0)
                
                if variable_name == 'flow':
                    data['flow'] = float(value)
                elif variable_name == 'total':
                    data['total'] = float(value)
                elif variable_name == 'level':
                    data['level'] = float(value)
                elif variable_name == 'pulses':
                    data['pulses'] = int(value)
            
            return data
            
        except Exception as e:
            logger.error(f"Error parseando respuesta de Tago: {str(e)}")
            return {}


class TDataProvider(BaseProvider):
    """Proveedor TData"""
    
    async def fetch_data(self, device_id: str) -> ProviderData:
        """Obtener datos del proveedor TData"""
        try:
            url = f"{self.config.api_endpoint}/telemetry/{device_id}"
            headers = {
                'X-API-Key': self.config.authentication['api_key'],
                'Content-Type': 'application/json'
            }
            
            response_data = await self._make_request(url, headers=headers)
            
            if response_data:
                parsed_data = self.parse_response(response_data)
                return ProviderData(
                    provider_name=self.config.name,
                    device_id=device_id,
                    timestamp=datetime.now(),
                    data=parsed_data,
                    success=True
                )
            else:
                return ProviderData(
                    provider_name=self.config.name,
                    device_id=device_id,
                    timestamp=datetime.now(),
                    data={},
                    success=False,
                    error_message="No se pudo obtener respuesta del servidor"
                )
                
        except Exception as e:
            logger.error(f"Error obteniendo datos de TData para {device_id}: {str(e)}")
            return ProviderData(
                provider_name=self.config.name,
                device_id=device_id,
                timestamp=datetime.now(),
                data={},
                success=False,
                error_message=str(e)
            )
    
    def parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parsear respuesta específica de TData"""
        try:
            return {
                'flow': float(response.get('caudal_actual', 0.0)),
                'total': float(response.get('volumen_total', 0.0)),
                'level': float(response.get('nivel_agua', 0.0)),
                'pulses': int(response.get('contador_pulsos', 0)),
                'timestamp': response.get('fecha_medicion', datetime.now().isoformat()),
                'device_id': response.get('id_equipo', ''),
                'send_dga': response.get('enviar_dga', False),
                'total_diff': response.get('diferencia_volumen', 0),
                'total_today_diff': response.get('volumen_hoy', 0)
            }
        except Exception as e:
            logger.error(f"Error parseando respuesta de TData: {str(e)}")
            return {}


class ThingsIOProvider(BaseProvider):
    """Proveedor ThingsIO"""
    
    async def fetch_data(self, device_id: str) -> ProviderData:
        """Obtener datos del proveedor ThingsIO"""
        try:
            url = f"{self.config.api_endpoint}/devices/{device_id}/data"
            headers = {
                'Device-ID': self.config.authentication['device_id'],
                'Content-Type': 'application/json'
            }
            
            response_data = await self._make_request(url, headers=headers)
            
            if response_data:
                parsed_data = self.parse_response(response_data)
                return ProviderData(
                    provider_name=self.config.name,
                    device_id=device_id,
                    timestamp=datetime.now(),
                    data=parsed_data,
                    success=True
                )
            else:
                return ProviderData(
                    provider_name=self.config.name,
                    device_id=device_id,
                    timestamp=datetime.now(),
                    data={},
                    success=False,
                    error_message="No se pudo obtener respuesta del servidor"
                )
                
        except Exception as e:
            logger.error(f"Error obteniendo datos de ThingsIO para {device_id}: {str(e)}")
            return ProviderData(
                provider_name=self.config.name,
                device_id=device_id,
                timestamp=datetime.now(),
                data={},
                success=False,
                error_message=str(e)
            )
    
    def parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parsear respuesta específica de ThingsIO"""
        try:
            return {
                'flow': float(response.get('flow_rate', 0.0)),
                'total': float(response.get('total_volume', 0.0)),
                'level': float(response.get('water_level', 0.0)),
                'pulses': int(response.get('pulse_count', 0)),
                'timestamp': response.get('measurement_timestamp', datetime.now().isoformat()),
                'device_id': response.get('device_identifier', ''),
                'send_dga': response.get('send_to_dga', False),
                'total_diff': response.get('volume_difference', 0),
                'total_today_diff': response.get('today_volume', 0)
            }
        except Exception as e:
            logger.error(f"Error parseando respuesta de ThingsIO: {str(e)}")
            return {}


class ProviderManager:
    """Gestor unificado de proveedores"""
    
    def __init__(self):
        self.config = telemetry_config
        self.providers = self._initialize_providers()
    
    def _initialize_providers(self) -> Dict[str, BaseProvider]:
        """Inicializar todos los proveedores"""
        providers = {}
        
        # Crear instancias de cada proveedor
        provider_classes = {
            'twin': TwinProvider,
            'nettra': NettraProvider,
            'novus': NovusProvider,
            'tago': TagoProvider,
            'tdata': TDataProvider,
            'thingsio': ThingsIOProvider
        }
        
        for provider_name, provider_class in provider_classes.items():
            provider_config = self.config.get_provider_config(provider_name)
            if provider_config and provider_config.enabled:
                providers[provider_name] = provider_class(provider_config)
        
        return providers
    
    async def fetch_data_from_provider(self, provider_name: str, 
                                     device_id: str) -> Optional[ProviderData]:
        """Obtener datos de un proveedor específico"""
        provider = self.providers.get(provider_name)
        if not provider:
            logger.error(f"Proveedor {provider_name} no encontrado o deshabilitado")
            return None
        
        try:
            return await provider.fetch_data(device_id)
        except Exception as e:
            logger.error(f"Error obteniendo datos de {provider_name}: {str(e)}")
            return None
    
    async def fetch_data_from_all_providers(self, device_id: str) -> List[ProviderData]:
        """Obtener datos de todos los proveedores habilitados"""
        tasks = []
        
        for provider_name in self.providers.keys():
            task = self.fetch_data_from_provider(provider_name, device_id)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filtrar resultados válidos
        valid_results = []
        for result in results:
            if isinstance(result, ProviderData):
                valid_results.append(result)
            elif isinstance(result, Exception):
                logger.error(f"Error en proveedor: {str(result)}")
        
        return valid_results
    
    def get_available_providers(self) -> List[str]:
        """Obtener lista de proveedores disponibles"""
        return list(self.providers.keys())
    
    async def close_all_sessions(self):
        """Cerrar todas las sesiones de los proveedores"""
        for provider in self.providers.values():
            if provider.session:
                await provider.session.close()


# Instancia global del gestor de proveedores
provider_manager = ProviderManager() 