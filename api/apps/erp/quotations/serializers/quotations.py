"""
Serializers for quotations.
"""
from rest_framework import serializers
from ..models import Quotation, QuotationItem


class QuotationItemSerializer(serializers.ModelSerializer):
    """Serializer for QuotationItem model."""
    cost_category_name = serializers.CharField(source='cost_category.name', read_only=True)
    
    class Meta:
        model = QuotationItem
        fields = '__all__'


class QuotationSerializer(serializers.ModelSerializer):
    """Serializer for Quotation model."""
    items = QuotationItemSerializer(many=True, read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    client_name = serializers.CharField(source='project.client.name', read_only=True)
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Quotation
        fields = '__all__'
    
    def get_items_count(self, obj):
        return obj.items.count()


class QuotationDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Quotation with nested items."""
    items = QuotationItemSerializer(many=True, read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    client_name = serializers.CharField(source='project.client.name', read_only=True)
    client_identifier = serializers.CharField(source='project.client.identifier', read_only=True)
    
    class Meta:
        model = Quotation
        fields = '__all__'


class QuotationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating quotations with items."""
    items = QuotationItemSerializer(many=True, required=False)
    
    class Meta:
        model = Quotation
        fields = '__all__'
    
    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        quotation = Quotation.objects.create(**validated_data)
        
        for item_data in items_data:
            QuotationItem.objects.create(quotation=quotation, **item_data)
        
        return quotation 