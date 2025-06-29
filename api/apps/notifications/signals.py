"""
Signals para detectar cambios y enviar notificaciones automáticamente
"""
import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone

from .services import (
    BankingNotifications, PaymentNotifications, QuotationNotifications,
    InvoiceNotifications, SupportNotifications, ProjectNotifications
)

logger = logging.getLogger(__name__)
User = get_user_model()


# =============================================================================
# BANKING SIGNALS
# =============================================================================

@receiver(post_save, sender='erp.Transaction')
def handle_transaction_save(sender, instance, created, **kwargs):
    """Manejar cambios en transacciones bancarias"""
    try:
        if created:
            # Notificar transacción creada
            users = _get_users_for_module('banking')
            BankingNotifications.transaction_processed(instance, users)
            
        elif instance.status == 'PROCESSED':
            # Notificar transacción procesada
            users = _get_users_for_module('banking')
            BankingNotifications.transaction_processed(instance, users)
            
    except Exception as e:
        logger.error(f"Error in transaction signal: {e}")


@receiver(post_save, sender='erp.BankAccount')
def handle_bank_account_save(sender, instance, created, **kwargs):
    """Manejar cambios en cuentas bancarias"""
    try:
        # Verificar saldo bajo (si se configura)
        if hasattr(instance, 'minimum_balance') and instance.current_balance < instance.minimum_balance:
            users = _get_users_for_module('banking')
            BankingNotifications.low_balance_alert(instance, users)
            
    except Exception as e:
        logger.error(f"Error in bank account signal: {e}")


# =============================================================================
# PAYMENTS SIGNALS
# =============================================================================

@receiver(post_save, sender='erp.Payment')
def handle_payment_save(sender, instance, created, **kwargs):
    """Manejar cambios en pagos"""
    try:
        if created:
            # Notificar pago creado
            users = _get_users_for_module('payments')
            PaymentNotifications.payment_received(instance, users)
            
        elif instance.status == 'COMPLETED':
            # Notificar pago completado
            users = _get_users_for_module('payments')
            PaymentNotifications.payment_received(instance, users)
            
    except Exception as e:
        logger.error(f"Error in payment signal: {e}")


@receiver(post_save, sender='erp.PaymentSchedule')
def handle_payment_schedule_save(sender, instance, created, **kwargs):
    """Manejar cambios en programación de pagos"""
    try:
        # Verificar pagos vencidos
        if instance.status == 'OVERDUE' or (
            instance.due_date < timezone.now().date() and 
            instance.status == 'PENDING'
        ):
            users = _get_users_for_module('payments')
            PaymentNotifications.payment_overdue(instance, users)
            
    except Exception as e:
        logger.error(f"Error in payment schedule signal: {e}")


# =============================================================================
# QUOTATIONS SIGNALS
# =============================================================================

@receiver(post_save, sender='erp.Quotation')
def handle_quotation_save(sender, instance, created, **kwargs):
    """Manejar cambios en cotizaciones"""
    try:
        if created:
            # Notificar cotización creada
            users = _get_users_for_module('quotations')
            QuotationNotifications.quotation_approved(instance, users)
            
        elif instance.status == 'APPROVED':
            # Notificar cotización aprobada
            users = _get_users_for_module('quotations')
            QuotationNotifications.quotation_approved(instance, users)
            
        elif instance.status == 'REJECTED':
            # Notificar cotización rechazada
            users = _get_users_for_module('quotations')
            QuotationNotifications.quotation_approved(instance, users)
            
    except Exception as e:
        logger.error(f"Error in quotation signal: {e}")


# =============================================================================
# INVOICING SIGNALS
# =============================================================================

@receiver(post_save, sender='erp.Invoice')
def handle_invoice_save(sender, instance, created, **kwargs):
    """Manejar cambios en facturas"""
    try:
        if created:
            # Notificar factura creada
            users = _get_users_for_module('invoicing')
            InvoiceNotifications.invoice_created(instance, users)
            
        elif instance.is_overdue:
            # Notificar factura vencida
            users = _get_users_for_module('invoicing')
            InvoiceNotifications.invoice_overdue(instance, users)
            
    except Exception as e:
        logger.error(f"Error in invoice signal: {e}")


# =============================================================================
# SUPPORT SIGNALS
# =============================================================================

@receiver(post_save, sender='support.Ticket')
def handle_ticket_save(sender, instance, created, **kwargs):
    """Manejar cambios en tickets de soporte"""
    try:
        if created:
            # Notificar ticket creado
            users = _get_users_for_module('support')
            SupportNotifications.ticket_assigned(instance, users)
            
        else:
            # Verificar cambio de estado
            old_status = getattr(instance, '_old_status', None)
            if old_status and old_status != instance.status:
                instance._old_status = instance.status
                users = _get_users_for_module('support')
                SupportNotifications.ticket_status_changed(instance, users)
                
    except Exception as e:
        logger.error(f"Error in ticket signal: {e}")


@receiver(post_save, sender='support.Ticket')
def handle_ticket_assignment(sender, instance, created, **kwargs):
    """Manejar asignación de tickets"""
    try:
        if instance.assigned_to and (created or instance.tracker.has_changed('assigned_to')):
            # Notificar asignación
            users = [instance.assigned_to] if instance.assigned_to else []
            SupportNotifications.ticket_assigned(instance, users)
            
    except Exception as e:
        logger.error(f"Error in ticket assignment signal: {e}")


# =============================================================================
# PROJECTS SIGNALS
# =============================================================================

@receiver(post_save, sender='erp.Project')
def handle_project_save(sender, instance, created, **kwargs):
    """Manejar cambios en proyectos"""
    try:
        if created:
            # Notificar proyecto creado
            users = _get_users_for_module('projects')
            ProjectNotifications.project_created(instance, users)
            
    except Exception as e:
        logger.error(f"Error in project signal: {e}")


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def _get_users_for_module(module: str):
    """
    Obtener usuarios que deben recibir notificaciones para un módulo específico
    """
    try:
        # Por ahora, retornar todos los usuarios activos
        # En el futuro, esto puede ser más sofisticado basado en roles y preferencias
        return list(User.objects.filter(is_active=True))
    except Exception as e:
        logger.error(f"Error getting users for module {module}: {e}")
        return []


def _get_project_users(project):
    """
    Obtener usuarios relacionados con un proyecto específico
    """
    try:
        users = set()
        
        # Usuarios asignados a tickets del proyecto
        from api.apps.support.models import Ticket
        ticket_users = User.objects.filter(
            assigned_tickets__project=project
        ).distinct()
        users.update(ticket_users)
        
        # Usuarios que crearon tickets del proyecto
        created_ticket_users = User.objects.filter(
            created_tickets__project=project
        ).distinct()
        users.update(created_ticket_users)
        
        return list(users)
        
    except Exception as e:
        logger.error(f"Error getting project users: {e}")
        return []


def _get_ticket_users(ticket):
    """
    Obtener usuarios relacionados con un ticket específico
    """
    try:
        users = set()
        
        if ticket.assigned_to:
            users.add(ticket.assigned_to)
        
        if ticket.created_by:
            users.add(ticket.created_by)
        
        # Usuarios del departamento
        if ticket.department:
            dept_users = User.objects.filter(
                # Asumiendo que hay un campo department en User
                # department=ticket.department
            ).distinct()
            users.update(dept_users)
        
        return list(users)
        
    except Exception as e:
        logger.error(f"Error getting ticket users: {e}")
        return [] 