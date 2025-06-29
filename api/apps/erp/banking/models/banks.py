"""
Models for banks and bank accounts.
"""
from django.db import models
from decimal import Decimal
from api.apps.common.models import BaseModel


class Bank(BaseModel):
    """
    Bancos disponibles para las cuentas
    """
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    swift_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='Chile')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Bank"
        verbose_name_plural = "Banks"
        db_table = 'erp_bank'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class BankAccount(BaseModel):
    """
    Cuentas bancarias de la empresa
    """
    class AccountType(models.TextChoices):
        CHECKING = 'CHECKING', 'Cuenta Corriente'
        SAVINGS = 'SAVINGS', 'Cuenta de Ahorro'
        BUSINESS = 'BUSINESS', 'Cuenta Empresarial'
        FOREIGN = 'FOREIGN', 'Cuenta Extranjera'

    class Currency(models.TextChoices):
        CLP = 'CLP', 'Peso Chileno'
        USD = 'USD', 'Dólar Estadounidense'
        EUR = 'EUR', 'Euro'
        PEN = 'PEN', 'Sol Peruano'

    name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=50, unique=True)
    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name='accounts'
    )
    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.CHECKING
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.CLP
    )
    initial_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    current_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Bank Account"
        verbose_name_plural = "Bank Accounts"
        db_table = 'erp_bank_account'
        ordering = ['bank__name', 'name']

    def __str__(self):
        return f"{self.name} - {self.bank.name} ({self.account_number})"

    def save(self, *args, **kwargs):
        # Si es una nueva cuenta, establecer balance inicial
        if not self.pk:
            self.current_balance = self.initial_balance
        super().save(*args, **kwargs) 