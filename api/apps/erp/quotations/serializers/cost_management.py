"""
Serializers for cost management.
"""
from rest_framework import serializers
from ..models import CostCenter, CostCategory, ProjectCost, CostEstimate


class CostCenterSerializer(serializers.ModelSerializer):
    """Serializer for CostCenter model."""
    
    class Meta:
        model = CostCenter
        fields = '__all__'


class CostCategorySerializer(serializers.ModelSerializer):
    """Serializer for CostCategory model."""
    cost_center_name = serializers.CharField(source='cost_center.name', read_only=True)
    
    class Meta:
        model = CostCategory
        fields = '__all__'


class ProjectCostSerializer(serializers.ModelSerializer):
    """Serializer for ProjectCost model."""
    cost_category_name = serializers.CharField(source='cost_category.name', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = ProjectCost
        fields = '__all__'


class CostEstimateSerializer(serializers.ModelSerializer):
    """Serializer for CostEstimate model."""
    cost_category_name = serializers.CharField(source='cost_category.name', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = CostEstimate
        fields = '__all__' 