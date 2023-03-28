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

from api.crm.models import Project, Client, EconomicActivity,TechnicalInfo, Employee, Note
from api.crm.serializers.clients import (ProjectModelSerializer,
                                        ClientModelSerializer,
                                        TechnicalInfoSerializer, 
                                        RetrieveClientModel,
                                        EconomicActivityModelSerializer,
                                        ExternalClientModelSerializer)



class ClientExternalViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):

    permission_classes = [AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    ordering = ('created', )
    queryset = Note.objects.all()
    serializer_class = ExternalClientModelSerializer
    
class EconomicActivityViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):

    permission_classes = [AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    ordering = ('created', )
    queryset = EconomicActivity.objects.all()
    serializer_class = EconomicActivityModelSerializer 

class ProjectViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):

    permission_classes = [AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    ordering = ('created', )
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer 

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
    
    
    @action(detail=False, methods=['post'])
    def technica_info_add(self, request):
        """User sign in."""
        serializer = TechnicalInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        data = {
            'technical_info': TechnicalInfoSerializer(data).data,
        }
        return Response(data, status=status.HTTP_201_CREATED)


    


    
