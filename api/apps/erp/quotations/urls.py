"""
URLs for quotations and cost management.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CostCenterViewSet, CostCategoryViewSet, QuotationViewSet,
    QuotationItemViewSet, ProjectCostViewSet, CostEstimateViewSet
)

router = DefaultRouter()
router.register(r'cost-centers', CostCenterViewSet)
router.register(r'cost-categories', CostCategoryViewSet)
router.register(r'quotations', QuotationViewSet)
router.register(r'quotation-items', QuotationItemViewSet)
router.register(r'project-costs', ProjectCostViewSet)
router.register(r'cost-estimates', CostEstimateViewSet)

app_name = 'erp_quotations'

urlpatterns = [
    path('', include(router.urls)),
] 