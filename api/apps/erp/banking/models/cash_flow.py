"""
Models for cash flow and bank reconciliation.
"""
from django.db import models
from decimal import Decimal
from api.apps.common.models import BaseModel


class CashFlow(BaseModel):
    """
    Flujo de caja por período
    """
    class Period(models.TextChoices):
        DAILY = 'DAILY', 'Diario'
        WEEKLY = 'WEEKLY', 'Semanal'
        MONTHLY = 'MONTHLY', 'Mensual'
        QUARTERLY = 'QUARTERLY', 'Trimestral'
        YEARLY = 'YEARLY', 'Anual'

    period_type = models.CharField(
        max_length=20,
        choices=Period.choices,
        default=Period.MONTHLY
    )
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Ingresos
    total_income = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    payment_income = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    transfer_income = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    other_income = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Gastos
    total_expenses = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    project_costs = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    operational_costs = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    transfer_expenses = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    other_expenses = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Balance
    net_cash_flow = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    opening_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    closing_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    class Meta:
        verbose_name = "Cash Flow"
        verbose_name_plural = "Cash Flows"
        db_table = 'erp_cash_flow'
        ordering = ['-start_date']
        unique_together = ['period_type', 'start_date', 'end_date']

    def __str__(self):
        return f"Cash Flow {self.period_type} - {self.start_date} to {self.end_date}"

    def save(self, *args, **kwargs):
        # Calcular flujo neto
        self.net_cash_flow = self.total_income - self.total_expenses
        self.closing_balance = self.opening_balance + self.net_cash_flow
        super().save(*args, **kwargs)


class BankReconciliation(BaseModel):
    """
    Conciliación bancaria
    """
    bank_account = models.ForeignKey(
        'erp.BankAccount',
        on_delete=models.CASCADE,
        related_name='reconciliations'
    )
    reconciliation_date = models.DateField()
    bank_balance = models.DecimalField(max_digits=15, decimal_places=2)
    book_balance = models.DecimalField(max_digits=15, decimal_places=2)
    difference = models.DecimalField(max_digits=15, decimal_places=2)
    is_reconciled = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Bank Reconciliation"
        verbose_name_plural = "Bank Reconciliations"
        db_table = 'erp_bank_reconciliation'
        ordering = ['-reconciliation_date']

    def __str__(self):
        return f"Reconciliation {self.bank_account.name} - {self.reconciliation_date}"

    def save(self, *args, **kwargs):
        # Calcular diferencia
        self.difference = self.bank_balance - self.book_balance
        super().save(*args, **kwargs) 