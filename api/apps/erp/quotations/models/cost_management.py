"""
Models for cost management and categorization.
"""
from django.db import models
from decimal import Decimal
from api.apps.common.models import BaseModel


class CostCenter(BaseModel):
    """
    Centro de costos para categorizar gastos y costos
    """
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Cost Center"
        verbose_name_plural = "Cost Centers"
        db_table = 'erp_cost_center'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class CostCategory(BaseModel):
    """
    Categorías de costos (mano de obra, materiales, equipos, etc.)
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cost_center = models.ForeignKey(
        CostCenter, 
        on_delete=models.CASCADE, 
        related_name='categories'
    )
    
    class Meta:
        verbose_name = "Cost Category"
        verbose_name_plural = "Cost Categories"
        db_table = 'erp_cost_category'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.cost_center.code})"


class ProjectCost(BaseModel):
    """
    Costos reales asociados a un proyecto
    """
    project = models.ForeignKey(
        'erp.Project',
        on_delete=models.CASCADE,
        related_name='costs'
    )
    cost_category = models.ForeignKey(
        CostCategory,
        on_delete=models.CASCADE,
        related_name='project_costs'
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    invoice_reference = models.CharField(max_length=100, blank=True)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Project Cost"
        verbose_name_plural = "Project Costs"
        db_table = 'erp_project_cost'
        ordering = ['-date']

    def __str__(self):
        return f"{self.description} - {self.project.name} (${self.amount})"


class CostEstimate(BaseModel):
    """
    Estimaciones de costos para planificación
    """
    project = models.ForeignKey(
        'erp.Project',
        on_delete=models.CASCADE,
        related_name='cost_estimates'
    )
    cost_category = models.ForeignKey(
        CostCategory,
        on_delete=models.CASCADE,
        related_name='cost_estimates'
    )
    estimated_amount = models.DecimalField(max_digits=12, decimal_places=2)
    actual_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    variance = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Cost Estimate"
        verbose_name_plural = "Cost Estimates"
        db_table = 'erp_cost_estimate'

    def save(self, *args, **kwargs):
        # Calcular varianza
        self.variance = self.actual_amount - self.estimated_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Estimate {self.cost_category.name} - {self.project.name}" 