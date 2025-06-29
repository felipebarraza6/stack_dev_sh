"""
Modelos Pydantic para el servicio de alertas
"""
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from enum import Enum
import json


class AlertType(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    SUCCESS = "success"


class AlertModule(str, Enum):
    TELEMETRY = "telemetry"
    BANKING = "banking"
    PAYMENTS = "payments"
    QUOTATIONS = "quotations"
    SUPPORT = "support"
    PROJECTS = "projects"
    SYSTEM = "system"
    CUSTOM = "custom"


class ConditionOperator(str, Enum):
    EQ = "eq"  # Igual a
    NE = "ne"  # Diferente a
    GT = "gt"  # Mayor que
    GTE = "gte"  # Mayor o igual que
    LT = "lt"  # Menor que
    LTE = "lte"  # Menor o igual que
    CONTAINS = "contains"  # Contiene
    NOT_CONTAINS = "not_contains"  # No contiene
    IN = "in"  # Está en lista
    NOT_IN = "not_in"  # No está en lista
    BETWEEN = "between"  # Entre valores
    IS_NULL = "is_null"  # Es nulo
    IS_NOT_NULL = "is_not_null"  # No es nulo


class ConditionFunction(str, Enum):
    AVG = "avg"  # Promedio
    SUM = "sum"  # Suma
    MIN = "min"  # Mínimo
    MAX = "max"  # Máximo
    COUNT = "count"  # Conteo
    STD = "std"  # Desviación estándar
    TREND = "trend"  # Tendencia
    CHANGE = "change"  # Cambio porcentual


class AlertFrequency(str, Enum):
    IMMEDIATE = "immediate"  # Inmediato
    MINUTE_1 = "minute_1"  # Cada minuto
    MINUTE_5 = "minute_5"  # Cada 5 minutos
    MINUTE_15 = "minute_15"  # Cada 15 minutos
    MINUTE_30 = "minute_30"  # Cada 30 minutos
    HOUR_1 = "hour_1"  # Cada hora
    HOUR_6 = "hour_6"  # Cada 6 horas
    HOUR_12 = "hour_12"  # Cada 12 horas
    DAY_1 = "day_1"  # Diario
    WEEK_1 = "week_1"  # Semanal


class AlertStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PAUSED = "paused"


class ExecutionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TRIGGERED = "triggered"
    NOT_TRIGGERED = "not_triggered"


class AlertCondition(BaseModel):
    """Modelo para condiciones de alerta"""
    variable_name: str = Field(..., description="Nombre de la variable a monitorear")
    operator: ConditionOperator = Field(..., description="Operador de comparación")
    value: Any = Field(..., description="Valor de comparación")
    function: Optional[ConditionFunction] = Field(None, description="Función a aplicar a la variable")
    time_window: Optional[int] = Field(None, description="Ventana de tiempo en minutos para la función")
    secondary_value: Optional[Any] = Field(None, description="Valor secundario (para operadores como 'between')")
    
    @validator('value')
    def validate_value(cls, v):
        """Validar que el valor sea serializable"""
        try:
            json.dumps(v)
            return v
        except (TypeError, ValueError):
            raise ValueError("Value must be JSON serializable")


class AlertAction(BaseModel):
    """Modelo para acciones de alerta"""
    action_type: str = Field(..., description="Tipo de acción (notification, webhook, email, etc.)")
    target: str = Field(..., description="Destino de la acción")
    template_name: Optional[str] = Field(None, description="Nombre de la plantilla de notificación")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Parámetros adicionales")
    
    @validator('parameters')
    def validate_parameters(cls, v):
        """Validar que los parámetros sean serializables"""
        try:
            json.dumps(v)
            return v
        except (TypeError, ValueError):
            raise ValueError("Parameters must be JSON serializable")


class AlertRule(BaseModel):
    """Modelo para reglas de alerta"""
    id: Optional[int] = None
    name: str = Field(..., description="Nombre de la regla de alerta")
    description: Optional[str] = Field(None, description="Descripción de la regla")
    module: AlertModule = Field(..., description="Módulo al que pertenece la alerta")
    alert_type: AlertType = Field(..., description="Tipo de alerta")
    conditions: List[AlertCondition] = Field(..., description="Lista de condiciones")
    actions: List[AlertAction] = Field(..., description="Lista de acciones a ejecutar")
    frequency: AlertFrequency = Field(..., description="Frecuencia de ejecución")
    status: AlertStatus = Field(default=AlertStatus.ACTIVE, description="Estado de la regla")
    is_active: bool = Field(default=True, description="Si la regla está activa")
    priority: int = Field(default=1, description="Prioridad de la regla (1-10)")
    cooldown_minutes: int = Field(default=0, description="Tiempo de espera entre alertas en minutos")
    last_execution: Optional[datetime] = None
    next_execution: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    
    @validator('conditions')
    def validate_conditions(cls, v):
        """Validar que haya al menos una condición"""
        if not v:
            raise ValueError("At least one condition is required")
        return v
    
    @validator('actions')
    def validate_actions(cls, v):
        """Validar que haya al menos una acción"""
        if not v:
            raise ValueError("At least one action is required")
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        """Validar prioridad entre 1 y 10"""
        if not 1 <= v <= 10:
            raise ValueError("Priority must be between 1 and 10")
        return v


class AlertExecution(BaseModel):
    """Modelo para ejecuciones de alerta"""
    id: Optional[int] = None
    rule_id: int = Field(..., description="ID de la regla ejecutada")
    status: ExecutionStatus = Field(..., description="Estado de la ejecución")
    triggered: bool = Field(default=False, description="Si la alerta fue disparada")
    execution_time: datetime = Field(..., description="Tiempo de ejecución")
    duration_ms: Optional[int] = None
    error_message: Optional[str] = None
    condition_results: Dict[str, bool] = Field(default_factory=dict, description="Resultados de cada condición")
    action_results: Dict[str, Any] = Field(default_factory=dict, description="Resultados de cada acción")
    variable_values: Dict[str, Any] = Field(default_factory=dict, description="Valores de variables en el momento de la ejecución")


class VariableData(BaseModel):
    """Modelo para datos de variables"""
    variable_name: str = Field(..., description="Nombre de la variable")
    value: Any = Field(..., description="Valor de la variable")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(), description="Timestamp del valor")
    source: Optional[str] = Field(None, description="Fuente de los datos")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadatos adicionales")
    
    @validator('value')
    def validate_value(cls, v):
        """Validar que el valor sea serializable"""
        try:
            json.dumps(v)
            return v
        except (TypeError, ValueError):
            raise ValueError("Value must be JSON serializable")


class AlertTemplate(BaseModel):
    """Modelo para plantillas de alerta"""
    id: int
    name: str
    module: AlertModule
    alert_type: AlertType
    subject_template: str
    message_template: str
    is_active: bool
    available_variables: Dict[str, str]
    created_at: datetime
    updated_at: datetime


class AlertStats(BaseModel):
    """Modelo para estadísticas de alertas"""
    total_rules: int
    active_rules: int
    total_executions: int
    successful_executions: int
    failed_executions: int
    triggered_alerts: int
    executions_by_status: Dict[str, int]
    alerts_by_type: Dict[str, int]
    alerts_by_module: Dict[str, int]


class AlertMetrics(BaseModel):
    """Modelo para métricas del servicio"""
    total_rules: int
    active_rules: int
    total_executions_today: int
    triggered_alerts_today: int
    average_execution_time_ms: float
    error_rate: float
    most_active_variables: List[Dict[str, Any]]
    top_triggered_rules: List[Dict[str, Any]]


class HealthCheck(BaseModel):
    """Modelo para health check"""
    status: str
    service: str
    timestamp: datetime
    connections: Dict[str, str]


class TestConditionRequest(BaseModel):
    """Modelo para probar condiciones"""
    condition: AlertCondition
    variable_data: List[VariableData]


class TestConditionResponse(BaseModel):
    """Modelo para respuesta de prueba de condición"""
    condition: AlertCondition
    result: bool
    evaluated_value: Any
    execution_time_ms: int
    details: Dict[str, Any] 