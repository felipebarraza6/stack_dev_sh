# Django REST Framework
from rest_framework import serializers

# Models
from api.crm.models import Client, Employee

# Serializers
from api.crm.serializers.employees import EmployeeModelSerializer

class RetrieveClientModel(serializers.ModelSerializer):
    
    employess = serializers.SerializerMethodField('get_employees')
    
    def get_employees(self, enterprise):
        qs = Employee.objects.filter(enterprise = enterprise)
        serializer = EmployeeModelSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Client
        fields = (
                        'id',
                        'created',
                        'modified',
                        
                        'type_client',

                        'name',
                        'rut',
                        'region',
                        'province',
                        'commune',
                        'address_exact',
                        'phone_number',
                        'email',

                        'administered',
                        'number_starts',
                        'date_jurisdiction',

                        'amount_regularized',
                        'flow_rates',
                        'category',
                        
                        'employess',
                        'is_active',   
        )
        

class ClientModelSerializer(serializers.ModelSerializer):
    
    type_client = serializers.ChoiceField(
        choices = ['Planta APR','Empresa','Municipio', 'Essbio','DOH']
    )

    class Meta: 
        model = Client
        fields = (
                        'id',
                        'created',
                        'modified',
                        
                        'type_client',

                        'name',
                        'rut',
                        'region',
                        'province',
                        'commune',
                        'address_exact',
                        'phone_number',
                        'email',

                        'administered',
                        'number_starts',
                        'date_jurisdiction',

                        'amount_regularized',
                        'flow_rates',
                        'category',

                        'is_active',                     
                          
                 )

class ClientShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'id',
            'name',
            'email',
            'phone_number'
        )

    