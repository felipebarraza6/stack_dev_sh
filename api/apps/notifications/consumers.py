"""
Consumers para WebSocket de notificaciones
"""
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    Consumer para manejar conexiones WebSocket de notificaciones
    """
    
    async def connect(self):
        """Manejar conexión WebSocket"""
        try:
            # Obtener parámetros de la URL
            self.user_id = self.scope['url_route']['kwargs'].get('user_id')
            self.project_id = self.scope['url_route']['kwargs'].get('project_id')
            self.ticket_id = self.scope['url_route']['kwargs'].get('ticket_id')
            
            # Autenticar usuario
            if self.scope['user'] == AnonymousUser():
                await self.close()
                return
            
            self.user = self.scope['user']
            
            # Unirse a grupos de notificación
            await self._join_groups()
            
            # Aceptar conexión
            await self.accept()
            
            logger.info(f"WebSocket connected for user {self.user.id}")
            
        except Exception as e:
            logger.error(f"Error in WebSocket connect: {e}")
            await self.close()
    
    async def disconnect(self, close_code):
        """Manejar desconexión WebSocket"""
        try:
            # Salir de grupos
            await self._leave_groups()
            logger.info(f"WebSocket disconnected for user {self.user.id}")
        except Exception as e:
            logger.error(f"Error in WebSocket disconnect: {e}")
    
    async def receive(self, text_data):
        """Manejar mensajes recibidos del cliente"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'notification.read':
                await self._mark_notification_read(data.get('notification_id'))
            elif message_type == 'notification.mark_all_read':
                await self._mark_all_notifications_read()
            elif message_type == 'notification.preferences':
                await self._update_preferences(data.get('preferences'))
            else:
                logger.warning(f"Unknown message type: {message_type}")
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    async def notification_message(self, event):
        """Enviar notificación al cliente"""
        try:
            await self.send(text_data=json.dumps({
                'type': 'notification',
                'notification_id': event['notification_id'],
                'subject': event['subject'],
                'message': event['message'],
                'priority': event['priority'],
                'module': event['module'],
                'timestamp': event['timestamp'],
                'metadata': event.get('metadata', {})
            }))
        except Exception as e:
            logger.error(f"Error sending notification message: {e}")
    
    async def _join_groups(self):
        """Unirse a grupos de notificación"""
        # Grupo general del usuario
        user_group = f"user_{self.user.id}"
        await self.channel_layer.group_add(user_group, self.channel_name)
        
        # Grupos específicos si se especifican
        if self.project_id:
            project_group = f"project_{self.project_id}"
            await self.channel_layer.group_add(project_group, self.channel_name)
        
        if self.ticket_id:
            ticket_group = f"ticket_{self.ticket_id}"
            await self.channel_layer.group_add(ticket_group, self.channel_name)
    
    async def _leave_groups(self):
        """Salir de grupos de notificación"""
        try:
            user_group = f"user_{self.user.id}"
            await self.channel_layer.group_discard(user_group, self.channel_name)
            
            if self.project_id:
                project_group = f"project_{self.project_id}"
                await self.channel_layer.group_discard(project_group, self.channel_name)
            
            if self.ticket_id:
                ticket_group = f"ticket_{self.ticket_id}"
                await self.channel_layer.group_discard(ticket_group, self.channel_name)
        except Exception as e:
            logger.error(f"Error leaving groups: {e}")
    
    @database_sync_to_async
    def _mark_notification_read(self, notification_id):
        """Marcar notificación como leída"""
        try:
            from .models import Notification
            notification = Notification.objects.get(
                id=notification_id,
                user=self.user
            )
            notification.status = Notification.Status.READ
            notification.read_at = timezone.now()
            notification.save()
            
            logger.info(f"Notification {notification_id} marked as read by user {self.user.id}")
            
        except ObjectDoesNotExist:
            logger.warning(f"Notification {notification_id} not found for user {self.user.id}")
        except Exception as e:
            logger.error(f"Error marking notification as read: {e}")
    
    @database_sync_to_async
    def _mark_all_notifications_read(self):
        """Marcar todas las notificaciones como leídas"""
        try:
            from .models import Notification
            from django.utils import timezone
            
            notifications = Notification.objects.filter(
                user=self.user,
                status=Notification.Status.SENT
            )
            
            count = notifications.update(
                status=Notification.Status.READ,
                read_at=timezone.now()
            )
            
            logger.info(f"Marked {count} notifications as read for user {self.user.id}")
            
        except Exception as e:
            logger.error(f"Error marking all notifications as read: {e}")
    
    @database_sync_to_async
    def _update_preferences(self, preferences):
        """Actualizar preferencias de notificación"""
        try:
            from .models import NotificationPreference
            
            for module, settings in preferences.items():
                preference, created = NotificationPreference.objects.get_or_create(
                    user=self.user,
                    module=module
                )
                
                # Actualizar configuraciones
                if 'email_enabled' in settings:
                    preference.email_enabled = settings['email_enabled']
                if 'websocket_enabled' in settings:
                    preference.websocket_enabled = settings['websocket_enabled']
                if 'settings' in settings:
                    preference.settings.update(settings['settings'])
                
                preference.save()
            
            logger.info(f"Updated notification preferences for user {self.user.id}")
            
        except Exception as e:
            logger.error(f"Error updating notification preferences: {e}")


class ProjectNotificationConsumer(NotificationConsumer):
    """
    Consumer específico para notificaciones de proyectos
    """
    
    async def connect(self):
        """Conectar a notificaciones de proyecto específico"""
        self.project_id = self.scope['url_route']['kwargs'].get('project_id')
        
        if not self.project_id:
            await self.close()
            return
        
        await super().connect()
    
    async def project_update(self, event):
        """Enviar actualización de proyecto"""
        await self.send(text_data=json.dumps({
            'type': 'project_update',
            'project_id': event['project_id'],
            'update_type': event['update_type'],
            'data': event['data'],
            'timestamp': event['timestamp']
        }))


class TicketNotificationConsumer(NotificationConsumer):
    """
    Consumer específico para notificaciones de tickets
    """
    
    async def connect(self):
        """Conectar a notificaciones de ticket específico"""
        self.ticket_id = self.scope['url_route']['kwargs'].get('ticket_id')
        
        if not self.ticket_id:
            await self.close()
            return
        
        await super().connect()
    
    async def ticket_update(self, event):
        """Enviar actualización de ticket"""
        await self.send(text_data=json.dumps({
            'type': 'ticket_update',
            'ticket_id': event['ticket_id'],
            'update_type': event['update_type'],
            'data': event['data'],
            'timestamp': event['timestamp']
        })) 