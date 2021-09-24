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
from api.crm.serializers.clients import ClientModelSerializer, RetrieveClientModel



class ClientViewSet(mixins.CreateModelMixin,
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
    queryset= Client.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RetrieveClientModel
        return ClientModelSerializer

   

    class ClientFilter(filters.FilterSet):
        

        class Meta:
            model = Client
            fields = {
               
                'name': ['exact', 'contains'],
                'is_active': ['exact'],

                'commune': ['exact', 'contains'],
                'province': ['exact', 'contains'],
                'region': ['exact', 'contains'],                

                "date_jurisdiction": ['exact', 'contains'],
                'type_client': ['exact'],


                #DATA FILTERS
                'created': ['contains', 'gte', 'lte', 'year', 'month', 'day', 'year__range', 'month__range', 'day__range', 'date__range'],                
             
                }

    filterset_class = ClientFilter

    


    