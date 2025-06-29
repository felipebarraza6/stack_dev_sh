"""
Models for quotations and pricing.
"""
from django.db import models
from decimal import Decimal
from api.apps.common.models import BaseModel


class Quotation(BaseModel):
    """
    Cotización para un proyecto específico
    """
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Borrador'
        SENT = 'SENT', 'Enviada'
        APPROVED = 'APPROVED', 'Aprobada'
        REJECTED = 'REJECTED', 'Rechazada'
        EXPIRED = 'EXPIRED', 'Expirada'
        CONVERTED = 'CONVERTED', 'Convertida a Proyecto'

    project = models.ForeignKey(
        'erp.Project',
        on_delete=models.CASCADE,
        related_name='quotations'
    )
    quotation_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.DRAFT
    )
    issue_date = models.DateField()
    valid_until = models.DateField()
    total_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    discount_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    discount_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    final_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Quotation"
        verbose_name_plural = "Quotations"
        db_table = 'erp_quotation'
        ordering = ['-issue_date']

    def __str__(self):
        return f"Quotation #{self.quotation_number} - {self.project.name}"

    def save(self, *args, **kwargs):
        # Calcular descuento y monto final
        if self.discount_percentage > 0:
            self.discount_amount = (self.total_amount * self.discount_percentage) / 100
        self.final_amount = self.total_amount - self.discount_amount
        super().save(*args, **kwargs)


class QuotationItem(BaseModel):
    """
    Items individuales de una cotización
    """
    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.CASCADE,
        related_name='items'
    )
    description = models.CharField(max_length=255)
    cost_category = models.ForeignKey(
        'erp.CostCategory',
        on_delete=models.CASCADE,
        related_name='quotation_items'
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1.00'))
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    estimated_cost = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    profit_margin = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    
    class Meta:
        verbose_name = "Quotation Item"
        verbose_name_plural = "Quotation Items"
        db_table = 'erp_quotation_item'

    def save(self, *args, **kwargs):
        # Calcular precio total y margen de ganancia
        self.total_price = self.quantity * self.unit_price
        if self.estimated_cost > 0:
            profit = self.total_price - self.estimated_cost
            self.profit_margin = (profit / self.total_price) * 100 if self.total_price > 0 else 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} - {self.quotation.quotation_number}" 