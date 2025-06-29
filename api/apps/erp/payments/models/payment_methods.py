"""
Models for payment methods and terms.
"""
from django.db import models
from api.apps.common.models import BaseModel


class PaymentMethod(BaseModel):
    """
    Métodos de pago disponibles
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"
        db_table = 'erp_payment_method'
        ordering = ['name']

    def __str__(self):
        return self.name


class PaymentTerm(BaseModel):
    """
    Términos de pago estándar
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    days_to_pay = models.PositiveIntegerField(default=30)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Payment Term"
        verbose_name_plural = "Payment Terms"
        db_table = 'erp_payment_term'
        ordering = ['days_to_pay']

    def __str__(self):
        return f"{self.name} ({self.days_to_pay} days)" 