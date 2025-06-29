"""
WebSocket routing configuration for SmartHydro API
"""
from django.urls import re_path
from api.apps.notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
    re_path(r'ws/notifications/(?P<user_id>\w+)/$', NotificationConsumer.as_asgi()),
    re_path(r'ws/project/(?P<project_id>\w+)/$', NotificationConsumer.as_asgi()),
    re_path(r'ws/ticket/(?P<ticket_id>\w+)/$', NotificationConsumer.as_asgi()),
] 