"""
Views for cost management.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum

from ..models import CostCenter, CostCategory, ProjectCost, CostEstimate
from ..serializers import (
    CostCenterSerializer, CostCategorySerializer,
    ProjectCostSerializer, CostEstimateSerializer
)


class CostCenterViewSet(viewsets.ModelViewSet):
    """ViewSet for CostCenter model."""
    queryset = CostCenter.objects.filter(is_active=True)
    serializer_class = CostCenterSerializer
    
    @action(detail=True, methods=['get'])
    def categories(self, request, pk=None):
        """Obtener categorías de un centro de costos."""
        cost_center = self.get_object()
        categories = cost_center.categories.all()
        serializer = CostCategorySerializer(categories, many=True)
        return Response(serializer.data)


class CostCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for CostCategory model."""
    queryset = CostCategory.objects.all()
    serializer_class = CostCategorySerializer
    
    def get_queryset(self):
        queryset = CostCategory.objects.all()
        cost_center_id = self.request.query_params.get('cost_center', None)
        if cost_center_id:
            queryset = queryset.filter(cost_center_id=cost_center_id)
        return queryset


class ProjectCostViewSet(viewsets.ModelViewSet):
    """ViewSet for ProjectCost model."""
    queryset = ProjectCost.objects.all()
    serializer_class = ProjectCostSerializer
    
    def get_queryset(self):
        queryset = ProjectCost.objects.all()
        project_id = self.request.query_params.get('project', None)
        category_id = self.request.query_params.get('category', None)
        
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if category_id:
            queryset = queryset.filter(cost_category_id=category_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Resumen de costos por proyecto."""
        project_id = request.query_params.get('project', None)
        if not project_id:
            return Response(
                {'error': 'Se requiere project_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        costs = ProjectCost.objects.filter(project_id=project_id)
        total_cost = costs.aggregate(total=Sum('amount'))['total'] or 0
        
        by_category = costs.values('cost_category__name').annotate(
            total=Sum('amount')
        )
        
        return Response({
            'total_cost': total_cost,
            'by_category': by_category
        })


class CostEstimateViewSet(viewsets.ModelViewSet):
    """ViewSet for CostEstimate model."""
    queryset = CostEstimate.objects.all()
    serializer_class = CostEstimateSerializer
    
    def get_queryset(self):
        queryset = CostEstimate.objects.all()
        project_id = self.request.query_params.get('project', None)
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset
    
    @action(detail=False, methods=['get'])
    def variance_analysis(self, request):
        """Análisis de varianzas entre estimado y real."""
        project_id = request.query_params.get('project', None)
        if not project_id:
            return Response(
                {'error': 'Se requiere project_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        estimates = CostEstimate.objects.filter(project_id=project_id)
        total_estimated = estimates.aggregate(total=Sum('estimated_amount'))['total'] or 0
        total_actual = estimates.aggregate(total=Sum('actual_amount'))['total'] or 0
        total_variance = estimates.aggregate(total=Sum('variance'))['total'] or 0
        
        return Response({
            'total_estimated': total_estimated,
            'total_actual': total_actual,
            'total_variance': total_variance,
            'variance_percentage': (total_variance / total_estimated * 100) if total_estimated > 0 else 0
        }) 