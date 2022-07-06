
from rest_framework import mixins, viewsets, status

from django_filters import rest_framework as filters

from rest_framework.permissions import (
   AllowAny,
   IsAuthenticated
)


from api.crm.models import Quotation, Well
from api.crm.serializers import QuotationsModelSerializer, WellsModelSerializer


class QuotationViewSet(mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    permissions = [AllowAny, ]
    filter_backends = (filters.DjangoFilterBackend,)
    ordering = ('created',)
    queryset = Quotation.objects.all()
    serializer_class = QuotationsModelSerializer

    class QuotationFilter(filters.FilterSet):
        class Meta:
            model = Quotation
            fields = {
                    'client': ['exact']
            }

    filterset_class = QuotationFilter


