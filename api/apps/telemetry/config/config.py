"""
Configuración Unificada del Sistema de Telemetría
Centraliza todas las configuraciones de variables y procesamiento
"""
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class VariableType(Enum):
    """Tipos de variables soportadas por el sistema"""
    FLOW = "flow"           # Caudal
    TOTAL = "total"         # Totalizado/Acumulado
    LEVEL = "level"         # Nivel freático
    PULSES = "pulses"       # Pulsos del contador


class ProcessingRule(Enum):
    """Reglas de procesamiento para validación de datos"""
    ZERO_TOTAL_RESET = "zero_total_reset"           # Resetear total cuando llega 0
    LEVEL_MAX_RESET = "level_max_reset"             # Resetear nivel cuando supera máximo
    FLOW_TOTAL_CONSISTENCY = "flow_total_consistency"  # Validar consistencia caudal-total
    LEVEL_ACCUMULATED_CONSISTENCY = "level_accumulated_consistency"  # Validar nivel-acumulado


@dataclass
class VariableConfig:
    """Configuración específica para cada variable"""
    name: str
    variable_type: VariableType
    unit: str
    min_value: float
    max_value: float
    processing_rules: List[ProcessingRule]
    validation_enabled: bool = True
    alert_threshold: Optional[float] = None
    reset_threshold: Optional[float] = None
    
    def __post_init__(self):
        """Validar configuración después de la inicialización"""
        if self.min_value >= self.max_value:
            raise ValueError(f"min_value debe ser menor que max_value para {self.name}")


@dataclass
class ProviderConfig:
    """Configuración para cada proveedor de datos"""
    name: str
    api_endpoint: str
    authentication: Dict[str, Any]
    timeout: int = 30
    retry_attempts: int = 3
    enabled: bool = True


class TelemetryConfig:
    """Configuración centralizada del sistema de telemetría"""
    
    def __init__(self):
        self.variables = self._initialize_variables()
        self.providers = self._initialize_providers()
        self.processing_settings = self._initialize_processing_settings()
    
    def _initialize_variables(self) -> Dict[str, VariableConfig]:
        """Inicializar configuraciones de variables"""
        return {
            "flow": VariableConfig(
                name="Caudal",
                variable_type=VariableType.FLOW,
                unit="l/s",
                min_value=0.0,
                max_value=1000.0,
                processing_rules=[ProcessingRule.FLOW_TOTAL_CONSISTENCY],
                alert_threshold=0.0,  # Alerta si caudal es 0
                reset_threshold=None
            ),
            "total": VariableConfig(
                name="Totalizado",
                variable_type=VariableType.TOTAL,
                unit="m³",
                min_value=0.0,
                max_value=999999.0,
                processing_rules=[ProcessingRule.ZERO_TOTAL_RESET],
                alert_threshold=None,
                reset_threshold=0.0  # Resetear cuando llega a 0
            ),
            "level": VariableConfig(
                name="Nivel Freático",
                variable_type=VariableType.LEVEL,
                unit="m",
                min_value=0.0,
                max_value=100.0,
                processing_rules=[ProcessingRule.LEVEL_MAX_RESET, ProcessingRule.LEVEL_ACCUMULATED_CONSISTENCY],
                alert_threshold=90.0,  # Alerta si nivel supera 90m
                reset_threshold=95.0   # Resetear cuando supera 95m
            ),
            "pulses": VariableConfig(
                name="Pulsos",
                variable_type=VariableType.PULSES,
                unit="pulses",
                min_value=0,
                max_value=999999,
                processing_rules=[],
                alert_threshold=None,
                reset_threshold=None
            )
        }
    
    def _initialize_providers(self) -> Dict[str, ProviderConfig]:
        """Inicializar configuraciones de proveedores"""
        return {
            "twin": ProviderConfig(
                name="Twin",
                api_endpoint="https://api.twin.com",
                authentication={"api_key": "your_api_key"},
                timeout=30,
                retry_attempts=3
            ),
            "nettra": ProviderConfig(
                name="Nettra",
                api_endpoint="https://api.nettra.com",
                authentication={"username": "user", "password": "pass"},
                timeout=45,
                retry_attempts=2
            ),
            "novus": ProviderConfig(
                name="Novus",
                api_endpoint="https://api.novus.com",
                authentication={"token": "your_token"},
                timeout=60,
                retry_attempts=4
            ),
            "tago": ProviderConfig(
                name="Tago",
                api_endpoint="https://api.tago.io",
                authentication={"device_token": "your_device_token"},
                timeout=30,
                retry_attempts=3
            ),
            "tdata": ProviderConfig(
                name="TData",
                api_endpoint="https://api.tdata.com",
                authentication={"api_key": "your_api_key"},
                timeout=40,
                retry_attempts=2
            ),
            "thingsio": ProviderConfig(
                name="ThingsIO",
                api_endpoint="https://api.thingsio.com",
                authentication={"device_id": "your_device_id"},
                timeout=35,
                retry_attempts=3
            )
        }
    
    def _initialize_processing_settings(self) -> Dict[str, Any]:
        """Inicializar configuraciones de procesamiento"""
        return {
            "batch_size": 100,  # Tamaño del lote para procesamiento
            "max_retries": 3,   # Máximo número de reintentos
            "timeout": 300,     # Timeout en segundos
            "enable_caching": True,  # Habilitar caché
            "cache_ttl": 3600,  # TTL del caché en segundos
            "enable_async": True,    # Procesamiento asíncrono
            "max_workers": 4,   # Máximo número de workers
            "alert_email_enabled": True,  # Habilitar alertas por email
            "log_level": "INFO"
        }
    
    def get_variable_config(self, variable_name: str) -> Optional[VariableConfig]:
        """Obtener configuración de una variable específica"""
        return self.variables.get(variable_name)
    
    def get_provider_config(self, provider_name: str) -> Optional[ProviderConfig]:
        """Obtener configuración de un proveedor específico"""
        return self.providers.get(provider_name)
    
    def validate_variable_data(self, variable_name: str, value: float) -> bool:
        """Validar si un valor está dentro del rango permitido para la variable"""
        config = self.get_variable_config(variable_name)
        if not config:
            logger.warning(f"Configuración no encontrada para variable: {variable_name}")
            return False
        
        if not config.validation_enabled:
            return True
        
        return config.min_value <= value <= config.max_value
    
    def should_reset_variable(self, variable_name: str, value: float) -> bool:
        """Determinar si una variable debe ser reseteada basado en su valor"""
        config = self.get_variable_config(variable_name)
        if not config or not config.reset_threshold:
            return False
        
        return value >= config.reset_threshold
    
    def should_alert_variable(self, variable_name: str, value: float) -> bool:
        """Determinar si debe enviarse una alerta para una variable"""
        config = self.get_variable_config(variable_name)
        if not config or not config.alert_threshold:
            return False
        
        return value >= config.alert_threshold


# Instancia global de configuración
telemetry_config = TelemetryConfig() 