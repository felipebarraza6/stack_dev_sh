"""
URLs for banking and cash flow management.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    BankViewSet, BankAccountViewSet, TransactionViewSet,
    CashFlowViewSet, BankReconciliationViewSet
)

router = DefaultRouter()
router.register(r'banks', BankViewSet)
router.register(r'accounts', BankAccountViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'cash-flows', CashFlowViewSet)
router.register(r'reconciliations', BankReconciliationViewSet)

app_name = 'erp_banking'

urlpatterns = [
    path('', include(router.urls)),
] 