"""
URLs para la API de notificaciones
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'preferences', views.NotificationPreferenceViewSet, basename='notification-preference')
router.register(r'templates', views.NotificationTemplateViewSet, basename='notification-template')
router.register(r'logs', views.NotificationLogViewSet, basename='notification-log')

urlpatterns = [
    path('', include(router.urls)),
] 