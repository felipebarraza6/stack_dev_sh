from math import perm
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import action

from rest_framework import generics
from rest_framework import mixins, viewsets, status
from datetime import datetime

# Filters
from django_filters import rest_framework as filters

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.crm.models import (
    ProfileClient as ProfileClientM,
    RegisterPersons as RegisterPersonsM,
    DataHistoryFact as DataHistoryFactM,
    InteractionDetail as Interaction,
)

from api.crm.serializers.client_profile import (
    ProfileClientSerializer,
    RegisterPersons,
    DataHistoryFact,
    InteractionDetailSerializer,
    RetrieveProfileClientSerializer
)


class ClientProfileViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    queryset = ProfileClientM.objects.all().order_by('name_client', )
    serializer_class = ProfileClientSerializer
    lookup_field = "id"
    # Filters
    filter_backends = (filters.DjangoFilterBackend,)

    class ProfileFilter(filters.FilterSet):
        class Meta:
            model = ProfileClientM
            fields = {
                "is_monitoring": ["exact"],
                "name_client": ["icontains"]
            }

    filterset_class = ProfileFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RetrieveProfileClientSerializer
        elif self.action == 'list':
            return RetrieveProfileClientSerializer
        else:
            return ProfileClientSerializer


class DataHistoryFactViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    queryset = DataHistoryFactM.objects.all()
    serializer_class = DataHistoryFact
    lookup_field = "id"

    class UserFilter(filters.FilterSet):
        class Meta:
            model = DataHistoryFactM
            fields = {"profile": ["exact"]}

    filterset_class = UserFilter

    filter_backends = (filters.DjangoFilterBackend,)
