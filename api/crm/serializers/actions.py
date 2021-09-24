# Django REST Framework
from rest_framework import serializers
from django_filters import rest_framework as filters


# Models
from api.crm.models import Action, TypeAction

# Serializers
from api.crm.serializers.users import UserModelSerializer
from api.crm.serializers.clients import ClientModelSerializer, ClientShortSerializer
from api.crm.serializers.employees import EmployeeListSerializer

# Utilities
from datetime import timedelta
from django.utils import timezone


class ActionModelSerializer(serializers.ModelSerializer):
    
    user = serializers.StringRelatedField()
    client = ClientShortSerializer()
    type_action = serializers.StringRelatedField()
    employee = EmployeeListSerializer()


    class Meta:
        model = Action
        fields = [
            'id',
            'user',
            'client',
            'type_action',
            'employee',
            'date',
            'note',
            'is_warning',
            'is_priority',
            'is_active',
            'is_complete',
            'date_complete',
            'created',
            'modified'
        ]          
        

class CreateActionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Action
        fields = [
            'id',
            'user',
            'client',
            'type_action',
            'employee',
            'date',
            'note',
            'is_warning',
            'is_priority',
            'is_active',
            'is_complete',
            'date_complete'
        ]          

    """def validate(self, data):
        
        now = timezone.now()
        if data['date'] < now:
            raise serializers.ValidationError('La fecha no puede ser inferior a la fecha de hoy.')

        return data"""


class UpdateActionSerializer(serializers.ModelSerializer):    
    user = UserModelSerializer(default=serializers.CurrentUserDefault())
    date = serializers.DateTimeField()    
    

    class Meta:
        model = Action
        fields = '__all__'


class FinishActionSerializer(serializers.ModelSerializer):

    date_complete = serializers.DateTimeField()

    class Meta:

        model = Action
        fields = ('is_complete', 'is_active', 'is_priority', 'date_complete')

    def validate(self, data):

        print("ok")

        action = self.context['view'].get_object()

        if action.is_complete == True:
            raise serializers.ValidationError('Esta accion ya se habia finalizado!')
            
        if action.is_active == False:
            raise serializers.ValidationError('No puedes finalizar una accion que no esta activa')            
        return data


class TypeActionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeAction
        fields = [
            'id',
            'description',
            'is_active',
            'created',
            'modified'
        ]
