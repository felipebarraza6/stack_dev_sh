"""URLs de Usuarios"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para usuarios
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')

# URLs de usuarios
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
] 