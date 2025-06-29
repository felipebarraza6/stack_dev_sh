"""
Views for quotations.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

from ..models import Quotation, QuotationItem
from ..serializers import (
    QuotationSerializer, QuotationItemSerializer,
    QuotationDetailSerializer, QuotationCreateSerializer
)


class QuotationViewSet(viewsets.ModelViewSet):
    """ViewSet for Quotation model."""
    queryset = Quotation.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuotationDetailSerializer
        elif self.action == 'create':
            return QuotationCreateSerializer
        return QuotationSerializer
    
    def get_queryset(self):
        queryset = Quotation.objects.all()
        
        # Filtros
        status_filter = self.request.query_params.get('status', None)
        project_id = self.request.query_params.get('project', None)
        client_id = self.request.query_params.get('client', None)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if client_id:
            queryset = queryset.filter(project__client_id=client_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def expired(self, request):
        """Obtener cotizaciones expiradas."""
        today = timezone.now().date()
        expired_quotations = self.get_queryset().filter(
            valid_until__lt=today,
            status__in=['DRAFT', 'SENT']
        )
        serializer = self.get_serializer(expired_quotations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Obtener cotizaciones que expiran pronto."""
        today = timezone.now().date()
        week_from_now = today + timedelta(days=7)
        expiring_quotations = self.get_queryset().filter(
            valid_until__range=[today, week_from_now],
            status__in=['DRAFT', 'SENT']
        )
        serializer = self.get_serializer(expiring_quotations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def convert_to_project(self, request, pk=None):
        """Convertir cotización a proyecto."""
        quotation = self.get_object()
        
        if quotation.status != Quotation.Status.APPROVED:
            return Response(
                {'error': 'Solo se pueden convertir cotizaciones aprobadas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Aquí iría la lógica para convertir a proyecto
        quotation.status = Quotation.Status.CONVERTED
        quotation.save()
        
        return Response({'message': 'Cotización convertida a proyecto'})


class QuotationItemViewSet(viewsets.ModelViewSet):
    """ViewSet for QuotationItem model."""
    queryset = QuotationItem.objects.all()
    serializer_class = QuotationItemSerializer
    
    def get_queryset(self):
        queryset = QuotationItem.objects.all()
        quotation_id = self.request.query_params.get('quotation', None)
        if quotation_id:
            queryset = queryset.filter(quotation_id=quotation_id)
        return queryset 