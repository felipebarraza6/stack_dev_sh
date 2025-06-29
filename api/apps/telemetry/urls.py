"""
URLs para la API de telemetría
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    MeasurementViewSet, MeasurementBatchViewSet, MeasurementQualityViewSet,
    VariableViewSet, CatchmentPointViewSet, SchemeViewSet
)

# Configurar router
router = DefaultRouter()
router.register(r'measurements', MeasurementViewSet, basename='measurement')
router.register(r'batches', MeasurementBatchViewSet, basename='batch')
router.register(r'quality', MeasurementQualityViewSet, basename='quality')
router.register(r'variables', VariableViewSet, basename='variable')
router.register(r'points', CatchmentPointViewSet, basename='point')
router.register(r'schemes', SchemeViewSet, basename='scheme')

app_name = 'telemetry'

urlpatterns = [
    # Incluir todas las rutas del router
    path('', include(router.urls)),
    
    # Endpoints adicionales específicos
    path('dashboard/', include([
        path('stats/', MeasurementViewSet.as_view({'get': 'stats'}), name='dashboard-stats'),
        path('time-series/', MeasurementViewSet.as_view({'post': 'time_series'}), name='time-series'),
        path('export/', MeasurementViewSet.as_view({'post': 'export'}), name='export'),
    ])),
    
    # Endpoints para lotes
    path('batches/', include([
        path('stats/', MeasurementBatchViewSet.as_view({'get': 'stats'}), name='batch-stats'),
    ])),
    
    # Endpoints para puntos específicos
    path('points/<int:pk>/', include([
        path('measurements/', CatchmentPointViewSet.as_view({'get': 'measurements'}), name='point-measurements'),
        path('activate/', CatchmentPointViewSet.as_view({'post': 'activate_telemetry'}), name='activate-telemetry'),
        path('deactivate/', CatchmentPointViewSet.as_view({'post': 'deactivate_telemetry'}), name='deactivate-telemetry'),
    ])),
    
    # Endpoints para variables específicas
    path('variables/<int:pk>/', include([
        path('measurements/', VariableViewSet.as_view({'get': 'measurements'}), name='variable-measurements'),
    ])),
    
    # Endpoints para esquemas específicos
    path('schemes/<int:pk>/', include([
        path('assign/', SchemeViewSet.as_view({'post': 'assign_to_points'}), name='assign-scheme'),
        path('remove/', SchemeViewSet.as_view({'post': 'remove_from_points'}), name='remove-scheme'),
    ])),
] 