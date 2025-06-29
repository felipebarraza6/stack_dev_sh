"""
Models for payments and payment schedules.
"""
from django.db import models
from decimal import Decimal
from api.apps.common.models import BaseModel


class Payment(BaseModel):
    """
    Pagos realizados por clientes
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        PROCESSING = 'PROCESSING', 'Procesando'
        COMPLETED = 'COMPLETED', 'Completado'
        FAILED = 'FAILED', 'Fallido'
        CANCELLED = 'CANCELLED', 'Cancelado'
        REFUNDED = 'REFUNDED', 'Reembolsado'

    class Type(models.TextChoices):
        INVOICE_PAYMENT = 'INVOICE_PAYMENT', 'Pago de Factura'
        ADVANCE_PAYMENT = 'ADVANCE_PAYMENT', 'Pago Anticipado'
        DEPOSIT = 'DEPOSIT', 'Depósito'
        REFUND = 'REFUND', 'Reembolso'

    project = models.ForeignKey(
        'erp.Project',
        on_delete=models.CASCADE,
        related_name='payments'
    )
    invoice = models.ForeignKey(
        'erp.Invoice',
        on_delete=models.CASCADE,
        related_name='payments',
        null=True,
        blank=True
    )
    payment_method = models.ForeignKey(
        'erp.PaymentMethod',
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    payment_type = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.INVOICE_PAYMENT
    )
    payment_date = models.DateField()
    reference_number = models.CharField(max_length=100, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    bank_transaction = models.ForeignKey(
        'erp.Transaction',
        on_delete=models.SET_NULL,
        related_name='payments',
        null=True,
        blank=True
    )
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        db_table = 'erp_payment'
        ordering = ['-payment_date']

    def __str__(self):
        return f"Payment ${self.amount} - {self.project.name}"


class PaymentSchedule(BaseModel):
    """
    Programación de pagos para proyectos
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        PAID = 'PAID', 'Pagado'
        OVERDUE = 'OVERDUE', 'Vencido'
        CANCELLED = 'CANCELLED', 'Cancelado'

    project = models.ForeignKey(
        'erp.Project',
        on_delete=models.CASCADE,
        related_name='payment_schedules'
    )
    quotation = models.ForeignKey(
        'erp.Quotation',
        on_delete=models.CASCADE,
        related_name='payment_schedules',
        null=True,
        blank=True
    )
    installment_number = models.PositiveIntegerField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        related_name='schedules',
        null=True,
        blank=True
    )
    description = models.CharField(max_length=255, blank=True)
    
    class Meta:
        verbose_name = "Payment Schedule"
        verbose_name_plural = "Payment Schedules"
        db_table = 'erp_payment_schedule'
        ordering = ['project', 'installment_number']

    def __str__(self):
        return f"Installment {self.installment_number} - {self.project.name}" 