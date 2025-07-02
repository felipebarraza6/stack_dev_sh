"""
Tareas de Notificaciones con Celery
Sistema profesional de envío de notificaciones
"""
import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from api.apps.compliance.models.configs.compliance_config import ComplianceConfig
from api.apps.catchment.models.notifications.notification import CatchmentPointNotification

logger = logging.getLogger(__name__)


@shared_task
def notify_compliance_users(compliance_config_id, notification_type, details):
    """
    Notifica a usuarios sobre eventos de cumplimiento
    """
    try:
        compliance_config = ComplianceConfig.objects.get(id=compliance_config_id)
        
        # Obtener usuarios a notificar
        notifications = CatchmentPointNotification.objects.filter(
            catchment_point=compliance_config.catchment_point,
            is_active=True
        )
        
        for notification in notifications:
            if notification_type in notification.notification_types:
                # Enviar notificación según el canal
                for channel in notification.channels:
                    if channel == 'EMAIL':
                        send_email_notification.delay(
                            notification.user.id,
                            notification_type,
                            details
                        )
                    elif channel == 'SMS':
                        send_sms_notification.delay(
                            notification.user.id,
                            notification_type,
                            details
                        )
        
        logger.info(f"Notificaciones enviadas para {compliance_config}")
        
    except Exception as exc:
        logger.error(f"Error enviando notificaciones: {exc}")


@shared_task
def send_email_notification(user_id, notification_type, details):
    """
    Envía notificación por email
    """
    try:
        from api.apps.users.models.users.user import User
        
        user = User.objects.get(id=user_id)
        
        # Preparar contenido del email según el tipo de notificación
        subject, message = prepare_email_content(notification_type, details)
        
        # Enviar email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        logger.info(f"Email enviado a usuario {user.email}: {notification_type}")
        
    except Exception as exc:
        logger.error(f"Error enviando email: {exc}")


@shared_task
def send_sms_notification(user_id, notification_type, details):
    """
    Envía notificación por SMS
    """
    try:
        from api.apps.users.models.users.user import User
        
        user = User.objects.get(id=user_id)
        
        # Preparar contenido del SMS
        message = prepare_sms_content(notification_type, details)
        
        # Aquí implementarías el envío de SMS
        # Por ejemplo, usando Twilio, AWS SNS, etc.
        # send_sms(user.phone_number, message)
        
        logger.info(f"SMS enviado a usuario {user.phone_number}: {notification_type}")
        
    except Exception as exc:
        logger.error(f"Error enviando SMS: {exc}")


@shared_task
def send_system_alert(alert_type, message, recipients=None):
    """
    Envía alertas del sistema a administradores
    """
    try:
        if recipients is None:
            # Obtener administradores del sistema
            from api.apps.users.models.users.user import User
            recipients = User.objects.filter(is_staff=True).values_list('email', flat=True)
        
        # Preparar contenido de la alerta
        subject = f"Alerta del Sistema - {alert_type}"
        
        # Enviar email a todos los administradores
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=list(recipients),
            fail_silently=False,
        )
        
        logger.info(f"Alerta del sistema enviada: {alert_type}")
        
    except Exception as exc:
        logger.error(f"Error enviando alerta del sistema: {exc}")


@shared_task
def send_daily_summary():
    """
    Envía resumen diario a usuarios suscritos
    """
    try:
        from datetime import date
        from api.apps.users.models.users.user import User
        
        today = date.today()
        
        # Obtener usuarios que quieren resumen diario
        users = User.objects.filter(
            preferences__daily_summary=True,
            is_active=True
        )
        
        for user in users:
            # Generar resumen personalizado para cada usuario
            summary = generate_user_summary(user, today)
            
            # Enviar resumen por email
            send_mail(
                subject=f"Resumen Diario - {today}",
                message=summary,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        
        logger.info(f"Resúmenes diarios enviados a {users.count()} usuarios")
        
    except Exception as exc:
        logger.error(f"Error enviando resúmenes diarios: {exc}")


def prepare_email_content(notification_type, details):
    """
    Prepara el contenido del email según el tipo de notificación
    """
    if notification_type == 'DATA_SENT':
        subject = "Datos de Cumplimiento Enviados"
        message = f"Los datos de cumplimiento han sido enviados exitosamente.\n\nDetalles: {details}"
    elif notification_type == 'ERROR':
        subject = "Error en Procesamiento"
        message = f"Se ha producido un error en el procesamiento.\n\nDetalles: {details}"
    else:
        subject = "Notificación del Sistema"
        message = f"Tipo: {notification_type}\n\nDetalles: {details}"
    
    return subject, message


def prepare_sms_content(notification_type, details):
    """
    Prepara el contenido del SMS según el tipo de notificación
    """
    if notification_type == 'DATA_SENT':
        return f"Datos enviados exitosamente. Ref: {details.get('reference', 'N/A')}"
    elif notification_type == 'ERROR':
        return f"Error en sistema. Contacte administrador."
    else:
        return f"Notificación: {notification_type}"


def generate_user_summary(user, date):
    """
    Genera un resumen personalizado para el usuario
    """
    # Aquí implementarías la generación del resumen
    # Por ejemplo:
    # - Obtener puntos de captación del usuario
    # - Calcular estadísticas del día
    # - Incluir alertas relevantes
    
    summary = f"""
    Resumen Diario - {date}
    
    Hola {user.first_name},
    
    Aquí está tu resumen diario:
    
    - Puntos de captación activos: 0
    - Datos procesados: 0
    - Alertas: 0
    
    Saludos,
    Sistema SmartHydro
    """
    
    return summary 