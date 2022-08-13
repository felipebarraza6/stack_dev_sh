from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import action

from rest_framework import status
from rest_framework import mixins, viewsets, status


from rest_framework import generics

# Filters
from django_filters import rest_framework as filters

# Permissions
from rest_framework.permissions import ( 
    AllowAny,
    IsAuthenticated
)

from api.crm.models import Client, Employee
from api.crm.serializers.employees import EmployeeModelSerializer, EmployeeListSerializer

class EmployeeViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin, 
                  mixins.UpdateModelMixin, 
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet,):

    def get_permissions(self):
           
        permissions = [IsAuthenticated]
           
        return [p() for p in permissions]
    
    filter_backends = (filters.DjangoFilterBackend,)
    ordering = ('created',)
    queryset= Employee.objects.all()
        

    def get_permissions(self):
            if self.action in ['list', 'create', 'update', 'partial_update', 'retrieve', 'destroy', 'finish']:
                permissions = [IsAuthenticated]
            else:
                permissions = [AllowAny]
            return [p() for p in permissions]

    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeListSerializer
        else:
            return EmployeeModelSerializer 

    class EmployeeFilter(filters.FilterSet):

        class Meta:
            model = Employee
            fields = {
               
                'enterprise': ['exact'],            
                'name': ['exact', 'contains'],
                'charge': ['exact'],
                'phone_number': ['exact', 'contains'],
                'email': ['exact', 'contains'],
                'is_active': ['exact'],

                #DATA FILTERS
                'created': ['contains', 'gte', 'lte', 'year', 'month', 'day', 'year__range', 'month__range', 'day__range', 'date__range'],                
             
                }

    filterset_class = EmployeeFilter

    


    
