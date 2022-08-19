from rest_framework import mixins, viewsets, generics

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from django_filters import rest_framework as filters
from api.crm.models import Webinars
from api.crm.serializers import WebinarsModelSerializer

class WebinarsViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [AllowAny,]
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = Webinars.objects.all()
    serializer_class = WebinarsModelSerializer
    lookup_field = 'id'

