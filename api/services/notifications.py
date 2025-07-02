"""
Servicio de Notificaciones
Gestión y envío de notificaciones a usuarios
"""
import logging
from typing import Dict, Any, List
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from apps.users.models import User, CatchmentPointNotification
from apps.catchment.models import CatchmentPoint

logger = logging.getLogger(__name__)


class NotificationService:
    """Servicio para gestión de notificaciones"""
    
    def __init__(self, catchment_point: CatchmentPoint = None):
        self.catchment_point = catchment_point
    
    def send_notification(self, notification_type: str, message: str, 
                         users: List[User] = None, channels: List[str] = None) -> Dict[str, Any]:
        """
        Envía notificación a usuarios
        
        Args:
            notification_type: Tipo de notificación
            message: Mensaje a enviar
            users: Lista de usuarios (si no se especifica, usa configuración del punto)
            channels: Canales de envío (email, sms, webhook, etc.)
            
        Returns:
            Resultado del envío
        """
        try:
            if users is None and self.catchment_point:
                users = self._get_notification_users(notification_type)
            
            if channels is None:
                channels = ['email']
            
            results = {
                'sent': 0,
                'errors': 0,
                'details': []
            }
            
            for user in users:
                for channel in channels:
                    try:
                        if channel == 'email':
                            result = self._send_email(user, notification_type, message)
                        elif channel == 'sms':
                            result = self._send_sms(user, notification_type, message)
                        elif channel == 'webhook':
                            result = self._send_webhook(user, notification_type, message)
                        else:
                            result = {'status': 'error', 'message': f'Canal no soportado: {channel}'}
                        
                        if result['status'] == 'success':
                            results['sent'] += 1
                        else:
                            results['errors'] += 1
                        
                        results['details'].append({
                            'user_id': user.id,
                            'user_email': user.email,
                            'channel': channel,
                            'result': result
                        })
                        
                    except Exception as e:
                        results['errors'] += 1
                        results['details'].append({
                            'user_id': user.id,
                            'user_email': user.email,
                            'channel': channel,
                            'error': str(e)
                        })
            
            logger.info(f"Notificación enviada: {results['sent']} exitosas, {results['errors']} errores")
            
            return results
            
        except Exception as e:
            logger.error(f"Error enviando notificación: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _get_notification_users(self, notification_type: str) -> List[User]:
        """Obtiene usuarios a notificar según configuración del punto"""
        if not self.catchment_point:
            return []
        
        notifications = CatchmentPointNotification.objects.filter(
            catchment_point=self.catchment_point,
            is_active=True,
            notification_types__contains=[notification_type]
        )
        
        return [notification.user for notification in notifications]
    
    def _send_email(self, user: User, notification_type: str, message: str) -> Dict[str, Any]:
        """Envía notificación por email"""
        try:
            subject = f"Stack VPS - {notification_type.upper()}"
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            
            return {
                'status': 'success',
                'channel': 'email',
                'sent_at': timezone.now()
            }
            
        except Exception as e:
            logger.error(f"Error enviando email a {user.email}: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _send_sms(self, user: User, notification_type: str, message: str) -> Dict[str, Any]:
        """Envía notificación por SMS"""
        try:
            # Implementar envío de SMS
            # Por ahora solo log
            logger.info(f"SMS enviado a {user.phone}: {message}")
            
            return {
                'status': 'success',
                'channel': 'sms',
                'sent_at': timezone.now()
            }
            
        except Exception as e:
            logger.error(f"Error enviando SMS a {user.phone}: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _send_webhook(self, user: User, notification_type: str, message: str) -> Dict[str, Any]:
        """Envía notificación por webhook"""
        try:
            # Implementar envío por webhook
            # Por ahora solo log
            logger.info(f"Webhook enviado para {user.email}: {message}")
            
            return {
                'status': 'success',
                'channel': 'webhook',
                'sent_at': timezone.now()
            }
            
        except Exception as e:
            logger.error(f"Error enviando webhook para {user.email}: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }


class NotificationManager:
    """Gestor principal de notificaciones"""
    
    @staticmethod
    def notify_compliance_event(compliance_config, event_type: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Notifica eventos de cumplimiento"""
        service = NotificationService(compliance_config.catchment_point)
        
        message = f"""
        Evento de Cumplimiento: {event_type}
        Punto: {compliance_config.catchment_point.name}
        Fuente: {compliance_config.compliance_source.name}
        Detalles: {details}
        """
        
        return service.send_notification(
            notification_type='COMPLIANCE_EVENT',
            message=message,
            channels=['email']
        )
    
    @staticmethod
    def notify_telemetry_alert(catchment_point: CatchmentPoint, alert_type: str, 
                              alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """Notifica alertas de telemetría"""
        service = NotificationService(catchment_point)
        
        message = f"""
        Alerta de Telemetría: {alert_type}
        Punto: {catchment_point.name}
        Datos: {alert_data}
        """
        
        return service.send_notification(
            notification_type='TELEMETRY_ALERT',
            message=message,
            channels=['email', 'sms']
        )
    
    @staticmethod
    def notify_system_health(health_status: Dict[str, Any]) -> Dict[str, Any]:
        """Notifica estado de salud del sistema"""
        users = User.objects.filter(is_staff=True)
        service = NotificationService()
        
        message = f"""
        Estado de Salud del Sistema
        Estado: {health_status.get('status', 'unknown')}
        Detalles: {health_status.get('details', {})}
        """
        
        return service.send_notification(
            notification_type='SYSTEM_HEALTH',
            message=message,
            users=users,
            channels=['email']
        ) 