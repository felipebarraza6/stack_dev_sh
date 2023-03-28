# Django REST Framework
from rest_framework import serializers

# Models
from api.crm.models import  Project, EconomicActivity, ExternalClient, TechnicalInfo, Client, Employee

# Serializers
from api.crm.serializers.employees import EmployeeModelSerializer

class ProjectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ExternalClientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalClient
        fields = '__all__'

class EconomicActivityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EconomicActivity
        fields = '__all__'

class RetrieveForClientModel(serializers.ModelSerializer):
    class Meta:
        model = TechnicalInfo
        fields = '__all__'


class RetrieveClientModel(serializers.ModelSerializer):
    
    employess = serializers.SerializerMethodField('get_employees')
    tech_info = serializers.SerializerMethodField('get_technical_info')
    
    def get_employees(self, enterprise):
        qs = Employee.objects.filter(enterprise = enterprise)
        serializer = EmployeeModelSerializer(instance=qs, many=True)
        return serializer.data

    def get_technical_info(self, client):
        qs = TechnicalInfo.objects.filter(client=client.id).first()
        serializer = RetrieveForClientModel(instance=qs, many=False)
        return serializer.data

    class Meta:
        model = Client
        fields = (
                'id',
                'created',
                'modified',
                'tech_info',
                
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
                'is_active'   
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

class TechnicalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalInfo
        fields = '__all__'
    
