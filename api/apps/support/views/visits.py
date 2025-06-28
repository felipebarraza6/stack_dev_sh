"""
Views for the FieldVisit model.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from api.apps.support.models import FieldVisit
from api.apps.support.serializers import FieldVisitSerializer

class FieldVisitViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing field visit instances.
    """
    queryset = FieldVisit.objects.all().select_related('ticket', 'technician')
    serializer_class = FieldVisitSerializer
    permission_classes = [IsAuthenticated]

    # Enable filtering
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'technician', 'ticket']
    ordering_fields = ['scheduled_date', 'start_time']
    ordering = ['-scheduled_date'] 