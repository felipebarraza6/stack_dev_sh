"""
Manager principal para el servicio de notificaciones
"""
import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import pytz
import httpx
from jinja2 import Template
import aioredis
import asyncpg

from .models import (
    NotificationStatus, NotificationPriority, NotificationModule,
    NotificationTemplate, Notification, NotificationPreference
)

logger = logging.getLogger(__name__)
CHILE_TZ = pytz.timezone('America/Santiago')


class NotificationManager:
    """
    Manager principal para manejar todas las operaciones de notificaciones
    """
    
    def __init__(self, database_url: str, redis_url: str, django_api_url: str):
        self.database_url = database_url
        self.redis_url = redis_url
        self.django_api_url = django_api_url
        
        # Conexiones
        self.db_pool: Optional[asyncpg.Pool] = None
        self.redis: Optional[aioredis.Redis] = None
        self.http_client: Optional[httpx.AsyncClient] = None
        
        # Configuración
        self.email_enabled = True
        self.websocket_enabled = True
    
    async def initialize(self):
        """Inicializar conexiones"""
        try:
            # Pool de base de datos
            self.db_pool = await asyncpg.create_pool(self.database_url)
            logger.info("Database pool created")
            
            # Redis para WebSocket
            self.redis = aioredis.from_url(self.redis_url)
            await self.redis.ping()
            logger.info("Redis connection established")
            
            # Cliente HTTP para comunicación con Django API
            self.http_client = httpx.AsyncClient(timeout=30.0)
            logger.info("HTTP client initialized")
            
        except Exception as e:
            logger.error(f"Error initializing notification manager: {e}")
            raise
    
    async def health_check(self) -> Dict[str, str]:
        """Verificar salud de las conexiones"""
        connections = {}
        
        try:
            # Verificar base de datos
            if self.db_pool:
                await self.db_pool.execute("SELECT 1")
                connections["database"] = "connected"
            else:
                connections["database"] = "disconnected"
        except Exception:
            connections["database"] = "error"
        
        try:
            # Verificar Redis
            if self.redis:
                await self.redis.ping()
                connections["redis"] = "connected"
            else:
                connections["redis"] = "disconnected"
        except Exception:
            connections["redis"] = "error"
        
        try:
            # Verificar Django API
            if self.http_client:
                response = await self.http_client.get(f"{self.django_api_url}/health/")
                if response.status_code == 200:
                    connections["django_api"] = "connected"
                else:
                    connections["django_api"] = "error"
            else:
                connections["django_api"] = "disconnected"
        except Exception:
            connections["django_api"] = "error"
        
        return connections
    
    async def send_notification(
        self,
        template_name: str,
        module: str,
        user_ids: List[int],
        context_data: Dict[str, Any],
        priority: str = "medium",
        related_model: Optional[str] = None,
        related_id: Optional[int] = None
    ):
        """Enviar notificación usando plantilla"""
        try:
            # Obtener plantilla
            template = await self._get_template(template_name, module)
            if not template:
                logger.error(f"Template not found: {template_name} for module {module}")
                return
            
            # Procesar usuarios
            for user_id in user_ids:
                # Verificar preferencias del usuario
                if not await self._should_send_notification(user_id, module):
                    continue
                
                # Crear notificación
                notification_id = await self._create_notification(
                    user_id, template, context_data, priority, related_model, related_id
                )
                
                # Enviar por canales configurados
                await self._send_by_channels(notification_id, template, context_data)
                
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
    
    async def send_custom_notification(
        self,
        subject: str,
        message: str,
        user_ids: List[int],
        priority: str = "medium",
        module: str = "global"
    ):
        """Enviar notificación personalizada sin plantilla"""
        try:
            for user_id in user_ids:
                # Verificar preferencias del usuario
                if not await self._should_send_notification(user_id, module):
                    continue
                
                # Crear notificación personalizada
                notification_id = await self._create_custom_notification(
                    user_id, subject, message, priority, module
                )
                
                # Enviar por canales configurados
                await self._send_custom_by_channels(notification_id, subject, message, priority)
                
        except Exception as e:
            logger.error(f"Error sending custom notification: {e}")
    
    async def _get_template(self, name: str, module: str) -> Optional[Dict]:
        """Obtener plantilla de la base de datos"""
        try:
            query = """
                SELECT id, name, module, notification_type, subject, message_template, 
                       is_active, available_variables
                FROM notifications_template 
                WHERE name = $1 AND module = $2 AND is_active = true
            """
            row = await self.db_pool.fetchrow(query, name, module)
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting template: {e}")
            return None
    
    async def _should_send_notification(self, user_id: int, module: str) -> bool:
        """Verificar si se debe enviar notificación al usuario"""
        try:
            query = """
                SELECT email_enabled, websocket_enabled 
                FROM notifications_preference 
                WHERE user_id = $1 AND module = $2
            """
            row = await self.db_pool.fetchrow(query, user_id, module)
            
            if row:
                return row['email_enabled'] or row['websocket_enabled']
            else:
                # Si no hay preferencias, usar configuración por defecto
                return True
                
        except Exception as e:
            logger.error(f"Error checking user preferences: {e}")
            return True
    
    async def _create_notification(
        self,
        user_id: int,
        template: Dict,
        context_data: Dict[str, Any],
        priority: str,
        related_model: Optional[str],
        related_id: Optional[int]
    ) -> int:
        """Crear registro de notificación"""
        try:
            # Renderizar plantilla
            subject_template = Template(template['subject'])
            message_template = Template(template['message_template'])
            
            subject = subject_template.render(**context_data)
            message = message_template.render(**context_data)
            
            # Insertar en base de datos
            query = """
                INSERT INTO notifications_notification 
                (user_id, template_id, subject, message, status, priority, 
                 related_model, related_id, metadata, created_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                RETURNING id
            """
            
            notification_id = await self.db_pool.fetchval(
                query,
                user_id,
                template['id'],
                subject,
                message,
                NotificationStatus.PENDING,
                priority,
                related_model,
                related_id,
                context_data,
                datetime.now(CHILE_TZ)
            )
            
            return notification_id
            
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            raise
    
    async def _create_custom_notification(
        self,
        user_id: int,
        subject: str,
        message: str,
        priority: str,
        module: str
    ) -> int:
        """Crear notificación personalizada"""
        try:
            query = """
                INSERT INTO notifications_notification 
                (user_id, template_id, subject, message, status, priority, 
                 related_model, metadata, created_at)
                VALUES ($1, NULL, $2, $3, $4, $5, $6, $7, $8)
                RETURNING id
            """
            
            notification_id = await self.db_pool.fetchval(
                query,
                user_id,
                subject,
                message,
                NotificationStatus.PENDING,
                priority,
                module,
                {"custom": True},
                datetime.now(CHILE_TZ)
            )
            
            return notification_id
            
        except Exception as e:
            logger.error(f"Error creating custom notification: {e}")
            raise
    
    async def _send_by_channels(self, notification_id: int, template: Dict, context_data: Dict):
        """Enviar notificación por los canales configurados"""
        try:
            # Obtener datos de la notificación
            notification = await self._get_notification(notification_id)
            if not notification:
                return
            
            user_id = notification['user_id']
            
            # Verificar preferencias del usuario
            preferences = await self._get_user_preferences(user_id, template['module'])
            
            # Enviar por email si está habilitado
            if template['notification_type'] in ['email', 'both'] and preferences.get('email_enabled', True):
                await self._send_email(notification_id, notification)
            
            # Enviar por WebSocket si está habilitado
            if template['notification_type'] in ['websocket', 'both'] and preferences.get('websocket_enabled', True):
                await self._send_websocket(notification_id, notification, context_data)
                
        except Exception as e:
            logger.error(f"Error sending by channels: {e}")
    
    async def _send_custom_by_channels(self, notification_id: int, subject: str, message: str, priority: str):
        """Enviar notificación personalizada por canales"""
        try:
            # Enviar por WebSocket (siempre habilitado para notificaciones personalizadas)
            await self._send_websocket_custom(notification_id, subject, message, priority)
            
        except Exception as e:
            logger.error(f"Error sending custom by channels: {e}")
    
    async def _send_email(self, notification_id: int, notification: Dict):
        """Enviar notificación por email"""
        try:
            # Obtener email del usuario desde Django API
            user_email = await self._get_user_email(notification['user_id'])
            if not user_email:
                return
            
            # Aquí implementarías el envío real de email
            # Por ahora solo log
            logger.info(f"Email sent to {user_email}: {notification['subject']}")
            
            # Actualizar estado
            await self._update_notification_status(notification_id, NotificationStatus.SENT)
            
            # Crear log
            await self._create_notification_log(notification_id, 'email', NotificationStatus.SENT)
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            await self._create_notification_log(notification_id, 'email', NotificationStatus.FAILED, str(e))
    
    async def _send_websocket(self, notification_id: int, notification: Dict, context_data: Dict):
        """Enviar notificación por WebSocket"""
        try:
            message = {
                'type': 'notification.message',
                'notification_id': notification_id,
                'subject': notification['subject'],
                'message': notification['message'],
                'priority': notification['priority'],
                'module': notification.get('related_model', 'global'),
                'timestamp': datetime.now(CHILE_TZ).isoformat(),
                'metadata': context_data
            }
            
            # Enviar al canal del usuario
            user_channel = f"user_{notification['user_id']}"
            await self.redis.publish(user_channel, str(message))
            
            # Actualizar estado
            await self._update_notification_status(notification_id, NotificationStatus.SENT)
            
            # Crear log
            await self._create_notification_log(notification_id, 'websocket', NotificationStatus.SENT)
            
        except Exception as e:
            logger.error(f"Error sending WebSocket notification: {e}")
            await self._create_notification_log(notification_id, 'websocket', NotificationStatus.FAILED, str(e))
    
    async def _send_websocket_custom(self, notification_id: int, subject: str, message: str, priority: str):
        """Enviar notificación personalizada por WebSocket"""
        try:
            # Obtener user_id de la notificación
            notification = await self._get_notification(notification_id)
            if not notification:
                return
            
            ws_message = {
                'type': 'notification.message',
                'notification_id': notification_id,
                'subject': subject,
                'message': message,
                'priority': priority,
                'module': 'global',
                'timestamp': datetime.now(CHILE_TZ).isoformat(),
                'metadata': {"custom": True}
            }
            
            # Enviar al canal del usuario
            user_channel = f"user_{notification['user_id']}"
            await self.redis.publish(user_channel, str(ws_message))
            
            # Actualizar estado
            await self._update_notification_status(notification_id, NotificationStatus.SENT)
            
            # Crear log
            await self._create_notification_log(notification_id, 'websocket', NotificationStatus.SENT)
            
        except Exception as e:
            logger.error(f"Error sending custom WebSocket notification: {e}")
            await self._create_notification_log(notification_id, 'websocket', NotificationStatus.FAILED, str(e))
    
    async def _get_notification(self, notification_id: int) -> Optional[Dict]:
        """Obtener notificación por ID"""
        try:
            query = "SELECT * FROM notifications_notification WHERE id = $1"
            row = await self.db_pool.fetchrow(query, notification_id)
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting notification: {e}")
            return None
    
    async def _get_user_email(self, user_id: int) -> Optional[str]:
        """Obtener email del usuario desde Django API"""
        try:
            response = await self.http_client.get(f"{self.django_api_url}/users/{user_id}/")
            if response.status_code == 200:
                user_data = response.json()
                return user_data.get('email')
            return None
        except Exception as e:
            logger.error(f"Error getting user email: {e}")
            return None
    
    async def _get_user_preferences(self, user_id: int, module: str) -> Dict:
        """Obtener preferencias del usuario"""
        try:
            query = """
                SELECT email_enabled, websocket_enabled, settings 
                FROM notifications_preference 
                WHERE user_id = $1 AND module = $2
            """
            row = await self.db_pool.fetchrow(query, user_id, module)
            return dict(row) if row else {"email_enabled": True, "websocket_enabled": True, "settings": {}}
        except Exception as e:
            logger.error(f"Error getting user preferences: {e}")
            return {"email_enabled": True, "websocket_enabled": True, "settings": {}}
    
    async def _update_notification_status(self, notification_id: int, status: str):
        """Actualizar estado de la notificación"""
        try:
            query = """
                UPDATE notifications_notification 
                SET status = $2, sent_at = $3 
                WHERE id = $1
            """
            await self.db_pool.execute(query, notification_id, status, datetime.now(CHILE_TZ))
        except Exception as e:
            logger.error(f"Error updating notification status: {e}")
    
    async def _create_notification_log(self, notification_id: int, channel: str, status: str, error_message: Optional[str] = None):
        """Crear log de notificación"""
        try:
            query = """
                INSERT INTO notifications_log 
                (notification_id, channel, status, sent_at, error_message, delivery_data)
                VALUES ($1, $2, $3, $4, $5, $6)
            """
            await self.db_pool.execute(
                query,
                notification_id,
                channel,
                status,
                datetime.now(CHILE_TZ),
                error_message,
                {}
            )
        except Exception as e:
            logger.error(f"Error creating notification log: {e}")
    
    # Métodos para la API REST
    async def get_user_notifications(
        self, user_id: int, status: Optional[str] = None, 
        module: Optional[str] = None, limit: int = 50, offset: int = 0
    ) -> List[Dict]:
        """Obtener notificaciones de un usuario"""
        try:
            conditions = ["user_id = $1"]
            params = [user_id]
            param_count = 1
            
            if status:
                param_count += 1
                conditions.append(f"status = ${param_count}")
                params.append(status)
            
            if module:
                param_count += 1
                conditions.append(f"related_model = ${param_count}")
                params.append(module)
            
            where_clause = " AND ".join(conditions)
            
            query = f"""
                SELECT * FROM notifications_notification 
                WHERE {where_clause}
                ORDER BY created_at DESC
                LIMIT ${param_count + 1} OFFSET ${param_count + 2}
            """
            params.extend([limit, offset])
            
            rows = await self.db_pool.fetch(query, *params)
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Error getting user notifications: {e}")
            return []
    
    async def mark_notification_read(self, notification_id: int) -> bool:
        """Marcar notificación como leída"""
        try:
            query = """
                UPDATE notifications_notification 
                SET status = $2, read_at = $3 
                WHERE id = $1
            """
            result = await self.db_pool.execute(
                query, notification_id, NotificationStatus.READ, datetime.now(CHILE_TZ)
            )
            return "UPDATE 1" in result
        except Exception as e:
            logger.error(f"Error marking notification as read: {e}")
            return False
    
    async def mark_all_notifications_read(self, user_id: int) -> int:
        """Marcar todas las notificaciones como leídas"""
        try:
            query = """
                UPDATE notifications_notification 
                SET status = $2, read_at = $3 
                WHERE user_id = $1 AND status = $4
            """
            result = await self.db_pool.execute(
                query, user_id, NotificationStatus.READ, datetime.now(CHILE_TZ), NotificationStatus.SENT
            )
            # Extraer número de filas actualizadas del resultado
            return int(result.split()[-1]) if "UPDATE" in result else 0
        except Exception as e:
            logger.error(f"Error marking all notifications as read: {e}")
            return 0
    
    async def get_unread_count(self, user_id: int) -> int:
        """Obtener conteo de notificaciones no leídas"""
        try:
            query = """
                SELECT COUNT(*) FROM notifications_notification 
                WHERE user_id = $1 AND status = $2
            """
            count = await self.db_pool.fetchval(query, user_id, NotificationStatus.SENT)
            return count or 0
        except Exception as e:
            logger.error(f"Error getting unread count: {e}")
            return 0
    
    async def get_user_notification_stats(self, user_id: int) -> Dict:
        """Obtener estadísticas de notificaciones"""
        try:
            # Total de notificaciones
            total_query = "SELECT COUNT(*) FROM notifications_notification WHERE user_id = $1"
            total = await self.db_pool.fetchval(total_query, user_id) or 0
            
            # No leídas
            unread_query = "SELECT COUNT(*) FROM notifications_notification WHERE user_id = $1 AND status = $2"
            unread = await self.db_pool.fetchval(unread_query, user_id, NotificationStatus.SENT) or 0
            
            # Por módulo
            module_query = """
                SELECT related_model, COUNT(*) 
                FROM notifications_notification 
                WHERE user_id = $1 
                GROUP BY related_model
            """
            module_rows = await self.db_pool.fetch(module_query, user_id)
            by_module = {row['related_model'] or 'global': row['count'] for row in module_rows}
            
            # Por estado
            status_query = """
                SELECT status, COUNT(*) 
                FROM notifications_notification 
                WHERE user_id = $1 
                GROUP BY status
            """
            status_rows = await self.db_pool.fetch(status_query, user_id)
            by_status = {row['status']: row['count'] for row in status_rows}
            
            # Por prioridad
            priority_query = """
                SELECT priority, COUNT(*) 
                FROM notifications_notification 
                WHERE user_id = $1 
                GROUP BY priority
            """
            priority_rows = await self.db_pool.fetch(priority_query, user_id)
            by_priority = {row['priority']: row['count'] for row in priority_rows}
            
            return {
                'total_notifications': total,
                'unread_notifications': unread,
                'notifications_by_module': by_module,
                'notifications_by_status': by_status,
                'notifications_by_priority': by_priority
            }
            
        except Exception as e:
            logger.error(f"Error getting notification stats: {e}")
            return {}
    
    async def get_templates(self, module: Optional[str] = None) -> List[Dict]:
        """Obtener plantillas de notificación"""
        try:
            if module:
                query = "SELECT * FROM notifications_template WHERE module = $1 AND is_active = true"
                rows = await self.db_pool.fetch(query, module)
            else:
                query = "SELECT * FROM notifications_template WHERE is_active = true"
                rows = await self.db_pool.fetch(query)
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Error getting templates: {e}")
            return []
    
    async def get_user_preferences(self, user_id: int) -> List[Dict]:
        """Obtener preferencias de notificación de un usuario"""
        try:
            query = "SELECT * FROM notifications_preference WHERE user_id = $1"
            rows = await self.db_pool.fetch(query, user_id)
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting user preferences: {e}")
            return []
    
    async def update_user_preferences(self, user_id: int, preferences: Dict[str, Any]) -> bool:
        """Actualizar preferencias de notificación de un usuario"""
        try:
            for module, settings in preferences.items():
                # Upsert preferencias
                query = """
                    INSERT INTO notifications_preference (user_id, module, email_enabled, websocket_enabled, settings)
                    VALUES ($1, $2, $3, $4, $5)
                    ON CONFLICT (user_id, module) 
                    DO UPDATE SET 
                        email_enabled = EXCLUDED.email_enabled,
                        websocket_enabled = EXCLUDED.websocket_enabled,
                        settings = EXCLUDED.settings,
                        updated_at = $6
                """
                
                await self.db_pool.execute(
                    query,
                    user_id,
                    module,
                    settings.get('email_enabled', True),
                    settings.get('websocket_enabled', True),
                    settings.get('settings', {}),
                    datetime.now(CHILE_TZ)
                )
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating user preferences: {e}")
            return False
    
    async def get_metrics(self) -> Dict:
        """Obtener métricas del servicio"""
        try:
            # Total de notificaciones enviadas
            total_query = "SELECT COUNT(*) FROM notifications_notification WHERE status = $1"
            total_sent = await self.db_pool.fetchval(total_query, NotificationStatus.SENT) or 0
            
            # Por canal
            channel_query = """
                SELECT channel, COUNT(*) 
                FROM notifications_log 
                WHERE status = $1 
                GROUP BY channel
            """
            channel_rows = await self.db_pool.fetch(channel_query, NotificationStatus.SENT)
            by_channel = {row['channel']: row['count'] for row in channel_rows}
            
            # Tasa de error
            error_query = "SELECT COUNT(*) FROM notifications_log WHERE status = $1"
            errors = await self.db_pool.fetchval(error_query, NotificationStatus.FAILED) or 0
            total_logs = await self.db_pool.fetchval("SELECT COUNT(*) FROM notifications_log") or 1
            error_rate = (errors / total_logs) * 100
            
            return {
                'total_notifications_sent': total_sent,
                'notifications_by_channel': by_channel,
                'average_delivery_time': 0.5,  # Placeholder
                'error_rate': error_rate,
                'active_websocket_connections': 0  # Placeholder
            }
            
        except Exception as e:
            logger.error(f"Error getting metrics: {e}")
            return {} 