"""
Models for payment receipts and approvals.
"""
from django.db import models
from api.apps.common.models import BaseModel


class PaymentReceipt(BaseModel):
    """
    Comprobantes de pago
    """
    payment = models.OneToOneField(
        'erp.Payment',
        on_delete=models.CASCADE,
        related_name='receipt'
    )
    receipt_number = models.CharField(max_length=50, unique=True)
    issued_date = models.DateField()
    file_path = models.CharField(max_length=500, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Payment Receipt"
        verbose_name_plural = "Payment Receipts"
        db_table = 'erp_payment_receipt'

    def __str__(self):
        return f"Receipt #{self.receipt_number}"


class PaymentApproval(BaseModel):
    """
    Aprobaciones de pagos cuando se requieren
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        APPROVED = 'APPROVED', 'Aprobado'
        REJECTED = 'REJECTED', 'Rechazado'

    payment = models.ForeignKey(
        'erp.Payment',
        on_delete=models.CASCADE,
        related_name='approvals'
    )
    approver = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='payment_approvals'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    approval_date = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Payment Approval"
        verbose_name_plural = "Payment Approvals"
        db_table = 'erp_payment_approval'
        ordering = ['-created_at']

    def __str__(self):
        return f"Approval for Payment {self.payment.pk} - {self.status}" 