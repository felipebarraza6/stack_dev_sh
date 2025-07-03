"""
URLs para API Base (Servicio Interno)
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Router para API base
base_router = DefaultRouter()

# URLs de API base
urlpatterns = [
    path('', include(base_router.urls)),
] 