"""
URLs for payment management.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PaymentMethodViewSet, PaymentViewSet, PaymentScheduleViewSet,
    PaymentTermViewSet, PaymentReceiptViewSet, PaymentApprovalViewSet
)

router = DefaultRouter()
router.register(r'payment-methods', PaymentMethodViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'payment-schedules', PaymentScheduleViewSet)
router.register(r'payment-terms', PaymentTermViewSet)
router.register(r'payment-receipts', PaymentReceiptViewSet)
router.register(r'payment-approvals', PaymentApprovalViewSet)

app_name = 'erp_payments'

urlpatterns = [
    path('', include(router.urls)),
] 