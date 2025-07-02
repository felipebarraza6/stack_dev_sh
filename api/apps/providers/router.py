"""URLs de Proveedores"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para proveedores
router = DefaultRouter()
router.register(r'providers', views.ProviderViewSet, basename='providers')
router.register(r'configs', views.ProviderConfigViewSet, basename='configs')
router.register(r'tokens', views.ProviderTokenViewSet, basename='tokens')

# URLs de proveedores
urlpatterns = [
    path('', include(router.urls)),
] 