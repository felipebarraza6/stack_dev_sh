"""
Modelos Pydantic para el servicio de notificaciones
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    READ = "read"


class NotificationType(str, Enum):
    EMAIL = "email"
    WEBSOCKET = "websocket"
    BOTH = "both"


class NotificationModule(str, Enum):
    BANKING = "banking"
    PAYMENTS = "payments"
    QUOTATIONS = "quotations"
    INVOICING = "invoicing"
    SUPPORT = "support"
    PROJECTS = "projects"
    GLOBAL = "global"


class NotificationRequest(BaseModel):
    """Modelo para solicitar envío de notificación"""
    template_name: str = Field(..., description="Nombre de la plantilla")
    module: NotificationModule = Field(..., description="Módulo del ERP")
    user_ids: List[int] = Field(..., description="IDs de usuarios a notificar")
    context_data: Dict[str, Any] = Field(default_factory=dict, description="Datos de contexto")
    priority: NotificationPriority = Field(default=NotificationPriority.MEDIUM, description="Prioridad")
    related_model: Optional[str] = Field(None, description="Modelo relacionado")
    related_id: Optional[int] = Field(None, description="ID del objeto relacionado")


class NotificationTemplate(BaseModel):
    """Modelo para plantillas de notificación"""
    id: int
    name: str
    module: NotificationModule
    notification_type: NotificationType
    subject: str
    message_template: str
    is_active: bool
    available_variables: Dict[str, str]
    created_at: datetime
    updated_at: datetime


class Notification(BaseModel):
    """Modelo para notificaciones"""
    id: int
    user_id: int
    template_id: int
    subject: str
    message: str
    status: NotificationStatus
    priority: NotificationPriority
    related_model: Optional[str]
    related_id: Optional[int]
    sent_at: Optional[datetime]
    read_at: Optional[datetime]
    metadata: Dict[str, Any]
    created_at: datetime


class NotificationPreference(BaseModel):
    """Modelo para preferencias de notificación"""
    id: int
    user_id: int
    module: NotificationModule
    email_enabled: bool
    websocket_enabled: bool
    settings: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


class NotificationLog(BaseModel):
    """Modelo para logs de notificación"""
    id: int
    notification_id: int
    channel: str
    status: NotificationStatus
    sent_at: datetime
    error_message: Optional[str]
    delivery_data: Dict[str, Any]


class NotificationStats(BaseModel):
    """Modelo para estadísticas de notificaciones"""
    total_notifications: int
    unread_notifications: int
    notifications_by_module: Dict[str, int]
    notifications_by_status: Dict[str, int]
    notifications_by_priority: Dict[str, int]


class HealthCheck(BaseModel):
    """Modelo para health check"""
    status: str
    service: str
    timestamp: datetime
    connections: Dict[str, str]


class Metrics(BaseModel):
    """Modelo para métricas del servicio"""
    total_notifications_sent: int
    notifications_by_channel: Dict[str, int]
    average_delivery_time: float
    error_rate: float
    active_websocket_connections: int 