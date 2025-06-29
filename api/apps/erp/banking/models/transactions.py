"""
Models for bank transactions.
"""
from django.db import models
from decimal import Decimal
from api.apps.common.models import BaseModel


class Transaction(BaseModel):
    """
    Transacciones bancarias
    """
    class TransactionType(models.TextChoices):
        DEPOSIT = 'DEPOSIT', 'Depósito'
        WITHDRAWAL = 'WITHDRAWAL', 'Retiro'
        TRANSFER_IN = 'TRANSFER_IN', 'Transferencia Entrante'
        TRANSFER_OUT = 'TRANSFER_OUT', 'Transferencia Saliente'
        PAYMENT = 'PAYMENT', 'Pago'
        RECEIPT = 'RECEIPT', 'Cobro'
        FEE = 'FEE', 'Comisión'
        INTEREST = 'INTEREST', 'Interés'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        PROCESSED = 'PROCESSED', 'Procesada'
        CANCELLED = 'CANCELLED', 'Cancelada'
        FAILED = 'FAILED', 'Fallida'

    bank_account = models.ForeignKey(
        'erp.BankAccount',
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_length=255)
    reference_number = models.CharField(max_length=100, blank=True)
    transaction_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    
    # Relaciones opcionales
    payment = models.ForeignKey(
        'erp.Payment',
        on_delete=models.SET_NULL,
        related_name='bank_transactions',
        null=True,
        blank=True
    )
    invoice = models.ForeignKey(
        'erp.Invoice',
        on_delete=models.SET_NULL,
        related_name='bank_transactions',
        null=True,
        blank=True
    )
    project = models.ForeignKey(
        'erp.Project',
        on_delete=models.SET_NULL,
        related_name='bank_transactions',
        null=True,
        blank=True
    )
    
    # Campos para transferencias entre cuentas
    destination_account = models.ForeignKey(
        'erp.BankAccount',
        on_delete=models.SET_NULL,
        related_name='incoming_transfers',
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        db_table = 'erp_transaction'
        ordering = ['-transaction_date', '-created_at']

    def __str__(self):
        return f"{self.transaction_type} - ${self.amount} - {self.bank_account.name}"

    def save(self, *args, **kwargs):
        # Actualizar balance de la cuenta
        if self.status == self.Status.PROCESSED:
            if self.transaction_type in [self.TransactionType.DEPOSIT, self.TransactionType.TRANSFER_IN, self.TransactionType.RECEIPT]:
                self.bank_account.current_balance += self.amount
            elif self.transaction_type in [self.TransactionType.WITHDRAWAL, self.TransactionType.TRANSFER_OUT, self.TransactionType.PAYMENT, self.TransactionType.FEE]:
                self.bank_account.current_balance -= self.amount
            
            self.bank_account.save()
        
        super().save(*args, **kwargs) 