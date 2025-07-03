"""
URLs para API Frontend (Capa Externa)
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Router para API frontend
frontend_router = DefaultRouter()

# URLs de API frontend
urlpatterns = [
    path('', include(frontend_router.urls)),
] 