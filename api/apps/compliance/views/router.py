"""URLs de Cumplimiento Regulatorio"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para cumplimiento
router = DefaultRouter()
router.register(r'compliance', views.ComplianceViewSet, basename='compliance')
router.register(r'reports', views.ReportViewSet, basename='reports')
router.register(r'validations', views.ValidationViewSet, basename='validations')

# URLs de cumplimiento
urlpatterns = [
    path('', include(router.urls)),
] 