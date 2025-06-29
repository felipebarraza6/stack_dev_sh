"""
Vistas para la API de notificaciones
"""
import logging
from django.utils import timezone
from django.db.models import Q, Count
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    NotificationTemplate, Notification, NotificationPreference, NotificationLog
)
from .serializers import (
    NotificationTemplateSerializer, NotificationSerializer,
    NotificationPreferenceSerializer, NotificationLogSerializer,
    NotificationStatsSerializer, NotificationBulkActionSerializer,
    NotificationFilterSerializer
)

logger = logging.getLogger(__name__)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para manejar notificaciones del usuario actual
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'template__module']
    search_fields = ['subject', 'message']
    ordering_fields = ['created_at', 'priority', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Obtener notificaciones del usuario actual"""
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Marcar notificación como leída"""
        try:
            notification = self.get_object()
            notification.status = Notification.Status.READ
            notification.read_at = timezone.now()
            notification.save()
            
            return Response({
                'message': 'Notificación marcada como leída',
                'notification_id': notification.id
            })
        except Exception as e:
            logger.error(f"Error marking notification as read: {e}")
            return Response(
                {'error': 'Error al marcar notificación como leída'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Marcar todas las notificaciones como leídas"""
        try:
            count = self.get_queryset().filter(
                status=Notification.Status.SENT
            ).update(
                status=Notification.Status.READ,
                read_at=timezone.now()
            )
            
            return Response({
                'message': f'{count} notificaciones marcadas como leídas',
                'count': count
            })
        except Exception as e:
            logger.error(f"Error marking all notifications as read: {e}")
            return Response(
                {'error': 'Error al marcar notificaciones como leídas'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def bulk_action(self, request):
        """Acción masiva en notificaciones"""
        serializer = NotificationBulkActionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            notification_ids = serializer.validated_data['notification_ids']
            action = serializer.validated_data['action']
            
            notifications = self.get_queryset().filter(id__in=notification_ids)
            
            if action == 'mark_read':
                count = notifications.update(
                    status=Notification.Status.READ,
                    read_at=timezone.now()
                )
                message = f'{count} notificaciones marcadas como leídas'
            elif action == 'mark_unread':
                count = notifications.update(
                    status=Notification.Status.SENT,
                    read_at=None
                )
                message = f'{count} notificaciones marcadas como no leídas'
            elif action == 'delete':
                count = notifications.count()
                notifications.delete()
                message = f'{count} notificaciones eliminadas'
            
            return Response({
                'message': message,
                'count': count
            })
            
        except Exception as e:
            logger.error(f"Error in bulk action: {e}")
            return Response(
                {'error': 'Error en acción masiva'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Obtener estadísticas de notificaciones"""
        try:
            queryset = self.get_queryset()
            
            stats = {
                'total_notifications': queryset.count(),
                'unread_notifications': queryset.filter(
                    status=Notification.Status.SENT
                ).count(),
                'notifications_by_module': dict(
                    queryset.values('template__module').annotate(
                        count=Count('id')
                    ).values_list('template__module', 'count')
                ),
                'notifications_by_status': dict(
                    queryset.values('status').annotate(
                        count=Count('id')
                    ).values_list('status', 'count')
                ),
                'notifications_by_priority': dict(
                    queryset.values('priority').annotate(
                        count=Count('id')
                    ).values_list('priority', 'count')
                )
            }
            
            serializer = NotificationStatsSerializer(stats)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error getting notification stats: {e}")
            return Response(
                {'error': 'Error al obtener estadísticas'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Obtener conteo de notificaciones no leídas"""
        try:
            count = self.get_queryset().filter(
                status=Notification.Status.SENT
            ).count()
            
            return Response({'unread_count': count})
            
        except Exception as e:
            logger.error(f"Error getting unread count: {e}")
            return Response(
                {'error': 'Error al obtener conteo'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar preferencias de notificación
    """
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Obtener preferencias del usuario actual"""
        return NotificationPreference.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Asignar usuario al crear preferencia"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def modules(self, request):
        """Obtener módulos disponibles"""
        from .models import NotificationTemplate
        modules = NotificationTemplate.Module.choices
        return Response({
            'modules': [{'value': value, 'label': label} for value, label in modules]
        })


class NotificationTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para plantillas de notificación (solo lectura)
    """
    queryset = NotificationTemplate.objects.filter(is_active=True)
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['module', 'notification_type']
    
    @action(detail=True, methods=['get'])
    def variables(self, request, pk=None):
        """Obtener variables disponibles para una plantilla"""
        template = self.get_object()
        return Response({
            'template_id': template.id,
            'available_variables': template.available_variables
        })


class NotificationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para logs de notificación (solo lectura)
    """
    serializer_class = NotificationLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['channel', 'status']
    ordering = ['-sent_at']
    
    def get_queryset(self):
        """Obtener logs de notificaciones del usuario actual"""
        return NotificationLog.objects.filter(
            notification__user=self.request.user
        ) 