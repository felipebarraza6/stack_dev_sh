# Django REST Framework
from rest_framework import serializers
from django_filters import rest_framework as filters

# Models
from api.crm.models.clients import Employee, Client


class EmployeeModelSerializer(serializers.ModelSerializer):    
    
    class Meta:
        model = Employee
        fields = (
            'id',
            'enterprise',
            'name',
            'charge',
            'phone_number',
            'email',
            'is_active'
        )

class EmployeeListSerializer(serializers.ModelSerializer):
    
    enterprise = serializers.StringRelatedField(many=False)       
 
    class Meta:
        model = Employee
        fields = (
            'id',
            'enterprise',
            'name',
            'charge',
            'phone_number',
            'email',
            'is_active'
        )