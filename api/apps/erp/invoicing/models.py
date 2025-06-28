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

    project = models.ForeignKey(
        'erp.Project',
        on_delete=models.CASCADE,
        related_name='invoices'
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT)
    issue_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
        db_table = 'erp_invoice'
        ordering = ['-issue_date']

    def __str__(self):
        project_name = getattr(self.project, 'name', 'N/A')
        return f"Invoice #{self.pk} for {project_name}"


class InvoiceItem(BaseModel):
    """
    Represents a single line item on an invoice.
    """
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items'
    )
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Invoice Item"
        verbose_name_plural = "Invoice Items"
        db_table = 'erp_invoice_item'

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} on {self.invoice}" 