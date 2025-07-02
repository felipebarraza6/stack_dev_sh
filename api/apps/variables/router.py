"""URLs de Variables"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para variables
router = DefaultRouter()
router.register(r'variables', views.VariableViewSet, basename='variables')
router.register(r'schemas', views.VariableSchemaViewSet, basename='schemas')
router.register(r'processing-rules', views.ProcessingRuleViewSet, basename='processing-rules')
router.register(r'data-points', views.DataPointViewSet, basename='data-points')
router.register(r'alerts', views.AlertViewSet, basename='alerts')

# URLs de variables
urlpatterns = [
    path('', include(router.urls)),
] 