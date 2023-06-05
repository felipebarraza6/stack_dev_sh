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

from api.crm.models import SectionElement, Project, TypeElement, ValueElement
from api.crm.serializers.projects import (SectionElementModelSerializer, ProjectModelSerializer, ProjectRetrieveModelSerializer,TypeElementModelSerializer, ValueElementSerializer)



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

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectRetrieveModelSerializer
        elif self.action == 'list':
            return ProjectRetrieveModelSerializer
        else:
            return ProjectModelSerializer

class TypeEelementViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):

    permission_classes = [AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    ordering = ('created', )
    queryset = TypeElement.objects.all()
    serializer_class = TypeElementModelSerializer

class ValueElementViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):

    permission_classes = [AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    ordering = ('created', )
    queryset = ValueElement.objects.all()
    serializer_class = ValueElementSerializer

    class ProjectFilter(filters.FilterSet):
        

        class Meta:
            model = ValueElement
            fields = {
                'project': ['exact'],                
                'user': ['exact'],
                'type_element': ['exact'],
            }

    filterset_class = ProjectFilter

class SectionElementViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):

    permission_classes = [AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    ordering = ('created', )
    queryset = SectionElement.objects.all()
    serializer_class = SectionElementModelSerializer
