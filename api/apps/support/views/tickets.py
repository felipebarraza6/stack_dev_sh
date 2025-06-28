"""
Views for the Ticket model.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from api.apps.support.models import Ticket
from api.apps.support.serializers import TicketSerializer

class TicketViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing ticket instances.
    Provides full CRUD functionality.
    """
    queryset = Ticket.objects.all().select_related(
        'department', 'created_by', 'assigned_to', 'catchment_point', 'project'
    ).prefetch_related('field_visits')
    
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    
    # Enable filtering and searching
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'department', 'assigned_to', 'project']
    search_fields = ['title', 'description']
    ordering_fields = ['priority', 'created_at', 'updated_at']
    ordering = ['-created_at'] 