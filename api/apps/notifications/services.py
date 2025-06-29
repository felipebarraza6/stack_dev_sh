"""
Servicio principal de notificaciones para SmartHydro ERP
"""
import logging
from typing import Dict, List, Optional, Any
from django.conf import settings
from django.core.mail import send_mail
from django.template import Template, Context
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

from .models import NotificationTemplate, Notification, NotificationPreference, NotificationLog

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Servicio principal para manejar notificaciones en todos los módulos del ERP
    """
    
    def __init__(self):
        self.channel_layer = get_channel_layer()
    
    def send_notification(
        self,
        template_name: str,
        module: str,
        users: List,
        context_data: Dict[str, Any],
        priority: str = 'medium',
        related_model: str = None,
        related_id: int = None
    ) -> List[Notification]:
        """
        Enviar notificación usando una plantilla específica
        """
        try:
            # Obtener plantilla
            template = NotificationTemplate.objects.get(
                name=template_name,
                module=module,
                is_active=True
            )
            
            notifications = []
            
            for user in users:
                # Verificar preferencias del usuario
                if not self._should_send_notification(user, module):
                    continue
                
                # Crear notificación
                notification = self._create_notification(
                    user, template, context_data, priority, related_model, related_id
                )
                
                # Enviar por canales configurados
                self._send_by_channels(notification, template, context_data)
                
                notifications.append(notification)
            
            return notifications
            
        except NotificationTemplate.DoesNotExist:
            logger.error(f"Template not found: {template_name} for module {module}")
            return []
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
            return []
    
    def _should_send_notification(self, user, module: str) -> bool:
        """Verificar si se debe enviar notificación al usuario"""
        try:
            preference = NotificationPreference.objects.get(user=user, module=module)
            return preference.email_enabled or preference.websocket_enabled
        except NotificationPreference.DoesNotExist:
            # Si no hay preferencias, usar configuración por defecto
            return True
    
    def _create_notification(
        self,
        user,
        template: NotificationTemplate,
        context_data: Dict[str, Any],
        priority: str,
        related_model: str = None,
        related_id: int = None
    ) -> Notification:
        """Crear registro de notificación"""
        
        # Renderizar plantilla
        template_obj = Template(template.message_template)
        context = Context(context_data)
        message = template_obj.render(context)
        
        # Renderizar asunto
        subject_template = Template(template.subject)
        subject = subject_template.render(context)
        
        return Notification.objects.create(
            user=user,
            template=template,
            subject=subject,
            message=message,
            priority=priority,
            related_model=related_model,
            related_id=related_id,
            metadata=context_data
        )
    
    def _send_by_channels(self, notification: Notification, template: NotificationTemplate, context_data: Dict):
        """Enviar notificación por los canales configurados"""
        
        if template.notification_type in ['email', 'both']:
            self._send_email(notification, context_data)
        
        if template.notification_type in ['websocket', 'both']:
            self._send_websocket(notification, context_data)
    
    def _send_email(self, notification: Notification, context_data: Dict):
        """Enviar notificación por email"""
        try:
            # Verificar preferencias del usuario
            preference = NotificationPreference.objects.filter(
                user=notification.user,
                module=notification.template.module
            ).first()
            
            if preference and not preference.email_enabled:
                return
            
            # Enviar email
            send_mail(
                subject=notification.subject,
                message=notification.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[notification.user.email],
                fail_silently=False,
            )
            
            # Actualizar estado
            notification.status = Notification.Status.SENT
            notification.sent_at = timezone.now()
            notification.save()
            
            # Crear log
            NotificationLog.objects.create(
                notification=notification,
                channel=NotificationLog.Channel.EMAIL,
                status=Notification.Status.SENT
            )
            
            logger.info(f"Email sent to {notification.user.email}: {notification.subject}")
            
        except Exception as e:
            logger.error(f"Error sending email to {notification.user.email}: {e}")
            self._log_failure(notification, 'email', str(e))
    
    def _send_websocket(self, notification: Notification, context_data: Dict):
        """Enviar notificación por WebSocket"""
        try:
            # Verificar preferencias del usuario
            preference = NotificationPreference.objects.filter(
                user=notification.user,
                module=notification.template.module
            ).first()
            
            if preference and not preference.websocket_enabled:
                return
            
            # Enviar por WebSocket
            message = {
                'type': 'notification.message',
                'notification_id': notification.id,
                'subject': notification.subject,
                'message': notification.message,
                'priority': notification.priority,
                'module': notification.template.module,
                'timestamp': timezone.now().isoformat(),
                'metadata': context_data
            }
            
            # Enviar al canal del usuario
            user_channel = f"user_{notification.user.id}"
            async_to_sync(self.channel_layer.group_send)(
                user_channel,
                message
            )
            
            # Actualizar estado
            notification.status = Notification.Status.SENT
            notification.sent_at = timezone.now()
            notification.save()
            
            # Crear log
            NotificationLog.objects.create(
                notification=notification,
                channel=NotificationLog.Channel.WEBSOCKET,
                status=Notification.Status.SENT
            )
            
            logger.info(f"WebSocket notification sent to user {notification.user.id}")
            
        except Exception as e:
            logger.error(f"Error sending WebSocket notification: {e}")
            self._log_failure(notification, 'websocket', str(e))
    
    def _log_failure(self, notification: Notification, channel: str, error_message: str):
        """Registrar fallo en el envío"""
        notification.status = Notification.Status.FAILED
        notification.save()
        
        NotificationLog.objects.create(
            notification=notification,
            channel=channel,
            status=Notification.Status.FAILED,
            error_message=error_message
        )


# Instancia global del servicio
notification_service = NotificationService()


# Funciones de conveniencia para cada módulo
class BankingNotifications:
    """Notificaciones específicas para el módulo Banking"""
    
    @staticmethod
    def transaction_processed(transaction, users: List):
        """Notificar transacción procesada"""
        context = {
            'transaction': transaction,
            'account': transaction.bank_account,
            'amount': transaction.amount,
            'type': transaction.get_transaction_type_display(),
            'date': transaction.transaction_date,
            'description': transaction.description
        }
        
        return notification_service.send_notification(
            template_name='transaction_processed',
            module='banking',
            users=users,
            context_data=context,
            priority='medium',
            related_model='erp.Transaction',
            related_id=transaction.id
        )
    
    @staticmethod
    def low_balance_alert(account, users: List):
        """Alerta de saldo bajo"""
        context = {
            'account': account,
            'current_balance': account.current_balance,
            'minimum_balance': account.minimum_balance if hasattr(account, 'minimum_balance') else 0
        }
        
        return notification_service.send_notification(
            template_name='low_balance_alert',
            module='banking',
            users=users,
            context_data=context,
            priority='high',
            related_model='erp.BankAccount',
            related_id=account.id
        )


class PaymentNotifications:
    """Notificaciones específicas para el módulo Payments"""
    
    @staticmethod
    def payment_received(payment, users: List):
        """Notificar pago recibido"""
        context = {
            'payment': payment,
            'project': payment.project,
            'amount': payment.amount,
            'method': payment.payment_method.name,
            'date': payment.payment_date,
            'reference': payment.reference_number
        }
        
        return notification_service.send_notification(
            template_name='payment_received',
            module='payments',
            users=users,
            context_data=context,
            priority='high',
            related_model='erp.Payment',
            related_id=payment.id
        )
    
    @staticmethod
    def payment_overdue(schedule, users: List):
        """Notificar pago vencido"""
        context = {
            'schedule': schedule,
            'project': schedule.project,
            'amount': schedule.amount,
            'due_date': schedule.due_date,
            'installment': schedule.installment_number
        }
        
        return notification_service.send_notification(
            template_name='payment_overdue',
            module='payments',
            users=users,
            context_data=context,
            priority='urgent',
            related_model='erp.PaymentSchedule',
            related_id=schedule.id
        )


class QuotationNotifications:
    """Notificaciones específicas para el módulo Quotations"""
    
    @staticmethod
    def quotation_approved(quotation, users: List):
        """Notificar cotización aprobada"""
        context = {
            'quotation': quotation,
            'project': quotation.project,
            'amount': quotation.final_amount,
            'number': quotation.quotation_number,
            'issue_date': quotation.issue_date
        }
        
        return notification_service.send_notification(
            template_name='quotation_approved',
            module='quotations',
            users=users,
            context_data=context,
            priority='high',
            related_model='erp.Quotation',
            related_id=quotation.id
        )
    
    @staticmethod
    def quotation_expiring(quotation, users: List):
        """Notificar cotización por expirar"""
        context = {
            'quotation': quotation,
            'project': quotation.project,
            'valid_until': quotation.valid_until,
            'number': quotation.quotation_number
        }
        
        return notification_service.send_notification(
            template_name='quotation_expiring',
            module='quotations',
            users=users,
            context_data=context,
            priority='medium',
            related_model='erp.Quotation',
            related_id=quotation.id
        )


class InvoiceNotifications:
    """Notificaciones específicas para el módulo Invoicing"""
    
    @staticmethod
    def invoice_created(invoice, users: List):
        """Notificar factura creada"""
        context = {
            'invoice': invoice,
            'project': invoice.project,
            'amount': invoice.total_amount,
            'number': invoice.invoice_number,
            'due_date': invoice.due_date
        }
        
        return notification_service.send_notification(
            template_name='invoice_created',
            module='invoicing',
            users=users,
            context_data=context,
            priority='medium',
            related_model='erp.Invoice',
            related_id=invoice.id
        )
    
    @staticmethod
    def invoice_overdue(invoice, users: List):
        """Notificar factura vencida"""
        context = {
            'invoice': invoice,
            'project': invoice.project,
            'amount': invoice.balance_amount,
            'number': invoice.invoice_number,
            'due_date': invoice.due_date
        }
        
        return notification_service.send_notification(
            template_name='invoice_overdue',
            module='invoicing',
            users=users,
            context_data=context,
            priority='urgent',
            related_model='erp.Invoice',
            related_id=invoice.id
        )


class SupportNotifications:
    """Notificaciones específicas para el módulo Support"""
    
    @staticmethod
    def ticket_assigned(ticket, users: List):
        """Notificar ticket asignado"""
        context = {
            'ticket': ticket,
            'title': ticket.title,
            'priority': ticket.get_priority_display(),
            'department': ticket.department.name if ticket.department else 'Sin departamento',
            'project': ticket.project.name if ticket.project else 'Sin proyecto'
        }
        
        return notification_service.send_notification(
            template_name='ticket_assigned',
            module='support',
            users=users,
            context_data=context,
            priority='high',
            related_model='support.Ticket',
            related_id=ticket.id
        )
    
    @staticmethod
    def ticket_status_changed(ticket, users: List):
        """Notificar cambio de estado en ticket"""
        context = {
            'ticket': ticket,
            'title': ticket.title,
            'old_status': getattr(ticket, '_old_status', 'Desconocido'),
            'new_status': ticket.get_status_display(),
            'project': ticket.project.name if ticket.project else 'Sin proyecto'
        }
        
        return notification_service.send_notification(
            template_name='ticket_status_changed',
            module='support',
            users=users,
            context_data=context,
            priority='medium',
            related_model='support.Ticket',
            related_id=ticket.id
        )


class ProjectNotifications:
    """Notificaciones específicas para el módulo Projects"""
    
    @staticmethod
    def project_created(project, users: List):
        """Notificar proyecto creado"""
        context = {
            'project': project,
            'client': project.client.name,
            'name': project.name,
            'code': project.internal_code
        }
        
        return notification_service.send_notification(
            template_name='project_created',
            module='projects',
            users=users,
            context_data=context,
            priority='medium',
            related_model='erp.Project',
            related_id=project.id
        ) 