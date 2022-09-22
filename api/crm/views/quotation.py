
from rest_framework import mixins, viewsets, status

from django_filters import rest_framework as filters

from rest_framework.permissions import (
   AllowAny,
   IsAuthenticated
)


from api.crm.models import Quotation, Well
from api.crm.serializers import QuotationRetrieveModelSerializer, QuotationsModelSerializer, WellsModelSerializer


class WellsViewSet(mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    permission_classes = [AllowAny, ]
    filter_backends = (filters.DjangoFilterBackend,)
    ordering = ('created',)
    queryset = Well.objects.all()
    serializer_class = WellsModelSerializer     
    class QuotationFilter(filters.FilterSet):

        class Meta:
            model = Well
            fields = {
                    'quotation': ['exact']
            }

    filterset_class = QuotationFilter



class QuotationViewSet(mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    permission_classes = [AllowAny, ]
    filter_backends = (filters.DjangoFilterBackend,)
    ordering = ('created',)
    queryset = Quotation.objects.all()
    serializer_class = QuotationsModelSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuotationRetrieveModelSerializer
        else:
            return QuotationsModelSerializer

    class QuotationFilter(filters.FilterSet):
        class Meta:
            model = Quotation
            fields = {
                    'client': ['exact']
            }

    filterset_class = QuotationFilter


