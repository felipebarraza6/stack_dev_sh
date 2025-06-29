"""
Models related to invoicing, such as invoices and their line items.
"""
from django.db import models
from decimal import Decimal
from api.apps.common.models import BaseModel

class Invoice(BaseModel):
    """
    Represents an invoice issued to a client for a project.
    """
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        SENT = 'SENT', 'Sent'
        PAID = 'PAID', 'Paid'
        CANCELLED = 'CANCELLED', 'Cancelled'
        OVERDUE = 'OVERDUE', 'Vencida'

    project = models.ForeignKey(
        'erp.Project',
        on_delete=models.CASCADE,
        related_name='invoices'
    )
    quotation = models.ForeignKey(
        'erp.Quotation',
        on_delete=models.SET_NULL,
        related_name='invoices',
        null=True,
        blank=True
    )
    invoice_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT)
    issue_date = models.DateField()
    due_date = models.DateField()
    payment_terms = models.ForeignKey(
        'erp.PaymentTerm',
        on_delete=models.SET_NULL,
        related_name='invoices',
        null=True,
        blank=True
    )
    subtotal = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'))
    paid_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'))
    balance_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'))
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
        db_table = 'erp_invoice'
        ordering = ['-issue_date']

    def __str__(self):
        project_name = getattr(self.project, 'name', 'N/A')
        return f"Invoice #{self.invoice_number} for {project_name}"

    def save(self, *args, **kwargs):
        # Calcular montos
        self.balance_amount = self.total_amount - self.paid_amount
        super().save(*args, **kwargs)

    @property
    def is_paid(self):
        """Verifica si la factura está completamente pagada"""
        return self.balance_amount <= 0

    @property
    def is_overdue(self):
        """Verifica si la factura está vencida"""
        from django.utils import timezone
        return self.due_date < timezone.now().date() and not self.is_paid


class InvoiceItem(BaseModel):
    """
    Represents a single line item on an invoice.
    """
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items'
    )
    quotation_item = models.ForeignKey(
        'erp.QuotationItem',
        on_delete=models.SET_NULL,
        related_name='invoice_items',
        null=True,
        blank=True
    )
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1.00'))
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    cost_category = models.ForeignKey(
        'erp.CostCategory',
        on_delete=models.SET_NULL,
        related_name='invoice_items',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Invoice Item"
        verbose_name_plural = "Invoice Items"
        db_table = 'erp_invoice_item'

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} on {self.invoice}" 