# Views Actions

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

from api.crm.permissions import IsAccountOwner

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from api.crm.models import Action, TypeAction
from api.crm.serializers.actions import (TypeActionModelSerializer, 
                                           ActionModelSerializer, 
                                           CreateActionSerializer, 
                                           FinishActionSerializer, 
                                           UpdateActionSerializer)

# Utilities
from datetime import timedelta
from django.utils import timezone

class ActionViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin, 
                  mixins.UpdateModelMixin, 
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet,):

    def get_permissions(self):
           
        permissions = [IsAuthenticated]
           
        return [p() for p in permissions]

    filter_backends = (filters.DjangoFilterBackend,)
    ordering = ('date',)
    search_fields = ('client', 'employee', 'date')
    queryset= Action.objects.all()

    class ActionFilter(filters.FilterSet):
        date = filters.IsoDateTimeFilter()
        class Meta:
            model = Action
            fields = {
                'user': ['exact'],
                'client': ['exact'],
                'type_action': ['exact'],
                'employee': ['exact'],
                'is_warning': ['exact'],
                'is_priority': ['exact'],
                'is_active': ['exact'],
                'is_complete': ['exact'],

                #DATA FILTERS
                'date_complete': ['contains', 'gte', 'lte', 'year', 'month', 'day', 'year__range', 'month__range', 'day__range', 'date__range'],
                'created': ['contains', 'gte', 'lte', 'year', 'month', 'day', 'year__range', 'month__range', 'day__range', 'date__range'],                
                'date': ['contains', 'gte', 'lte', 'year', 'month', 'day', 'year__range', 'month__range', 'day__range', 'date__range']
                }

         

    filterset_class = ActionFilter

    def get_serializer_class(self):
            if self.action == 'create':
                return CreateActionSerializer
            if self.action == 'finish':
                return FinishActionSerializer
            if self.action == 'update' or self.action == 'partial_update':
                return UpdateActionSerializer

            return ActionModelSerializer

    

    @action(detail=True, methods=['post'])
    def finish(self, request, *args, **kwargs):

        action = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            action,
            data = { 'is_active': False, 'is_complete': True, 'is_priority': False, 'date_complete': timezone.now()},
            context=self.get_serializer_context(),
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        action = serializer.save()
        data = ActionModelSerializer(action).data
        return Response(data)

    
        
    
class TypeActionViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin, 
                        mixins.UpdateModelMixin, 
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    def get_permissions(self):
        if self.action in ['list', 'create', 'update', 'partial_update', 'retrieve', 'destroy']:
            permissions = [IsAuthenticated]
        else:
            permissions = [AllowAny]
        return [p() for p in permissions]

    queryset = TypeAction.objects.all()
    serializer_class = TypeActionModelSerializer
    lookup_field = 'id'
    # Filters    
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('is_active',)

    class ActionTypeFilter(filters.FilterSet):        
        class Meta:
            model = TypeAction
            fields = {
                'description': ['contains']
                }

         

    filterset_class = ActionTypeFilter
