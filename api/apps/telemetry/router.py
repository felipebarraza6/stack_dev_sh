"""
Router para endpoints de Telemetría
Configura las rutas para el sistema de telemetría mejorado
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para telemetría
router = DefaultRouter()
router.register(r'telemetry', views.TelemetryViewSet, basename='telemetry')

# URLs de telemetría
urlpatterns = [
    path('', include(router.urls)),
    path('metrics/', views.metrics_view, name='telemetry-metrics'),
    path('dashboard/', views.TelemetryViewSet.as_view({'get': 'dashboard'}), name='telemetry-dashboard'),
    path('monthly-summary/', views.TelemetryViewSet.as_view({'get': 'monthly_summary'}), name='telemetry-monthly-summary'),
    path('point-details/', views.TelemetryViewSet.as_view({'get': 'point_details'}), name='telemetry-point-details'),
    path('alerts/', views.TelemetryViewSet.as_view({'get': 'alerts'}), name='telemetry-alerts'),
    path('system-status/', views.TelemetryViewSet.as_view({'get': 'system_status'}), name='telemetry-system-status'),
] 