from rest_framework import mixins, viewsets, generics
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from django_filters import rest_framework as filters
from api.crm.models import ProfileFootprints
from api.crm.serializers import ProfileFootprintsSerializer


class ProfileFootprintsViewSet(mixins.RetrieveModelMixin,
                               mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.UpdateModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = [AllowAny,]
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = ProfileFootprints.objects.all()
    serializer_class = ProfileFootprintsSerializer
    lookup_field = 'id'
