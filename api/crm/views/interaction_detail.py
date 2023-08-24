from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer

from api.crm.serializers import InteractionDetailModelSerializer 
from api.crm.models import InteractionDetail
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets, status

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import ( 
    AllowAny,
    IsAuthenticated
)




class OverridePagination(PageNumberPagination):       
               page_size = 10000

class InteractionDetailViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    ordering = ('created', )
    queryset = InteractionDetail.objects.all()
    serializer_class = InteractionDetailModelSerializer

    class InteractionFilter(filters.FilterSet):
        class Meta:
            model = InteractionDetail
            fields = {
                'profile_client': ['exact'],
                'is_send_dga': ['exact'],
                'created': ['contains', 'gte', 'lte', 'year', 'month', 'day', 'year__range', 'month__range', 'day__range', 'date__range'],                
            }

    filterset_class = InteractionFilter



class InteractionXLS(XLSXFileMixin, ReadOnlyModelViewSet):
    queryset = InteractionDetail.objects.all()
    serializer_class = InteractionDetailModelSerializer
    renderer_classes = (XLSXRenderer,)
    filename = 'reporte.xlsx'
    filter_backends = (filters.DjangoFilterBackend,)    
    pagination_class = OverridePagination

    class InteractionFilter(filters.FilterSet):
        class Meta:
            model = InteractionDetail
            fields = {
                'profile_client': ['exact'],            
                'created': ['contains', 'gte', 'lte', 'year', 'month', 'day', 'year__range', 'month__range', 'day__range', 'date__range'],                
            }

    filterset_class = InteractionFilter

    xlsx_ignore_headers = ['modified', 'id', 'date_time_medition', 'profile_client']
    column_header = {
        'titles': [
            "FECHA",
            "CAUDAL",
            "ACUMULADO",
            "NIVEL"
        ]
    }

