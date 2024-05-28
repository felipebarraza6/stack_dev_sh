from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer
from rest_framework.decorators import action

from api.core_app.serializers import InteractionDetailModelSerializer
from api.core_app.models import InteractionDetail
import xml.etree.ElementTree as ET

from zeep import Client
import requests
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets, status

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from api.core_app.cronjobs_dga.send_data_dga import send
import json


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

    @action(detail=False, methods=['post'])
    def send_data_dga(self, request):
        url = "https://snia.mop.gob.cl/controlextraccion/datosExtraccion/SendDataExtraccionService"
        data = request.data

        totalizador = int(data['totalizador'])
        rut = '17352192-8'
        password = 'ZSQgCiDg7y'
        caudal = float(data['caudal'])
        nivel_freatico_del_pozo = float(request.data['nivel'])
        codigo_obra = data['obra']
        time_stamp_origen = data['time_stamp_origen']
        fecha_medicion = data['fecha_medicion']
        hora_medicion = data['hora_medicion']

        """
        # serializer = UserSignUpSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # user = serializer.save()
        # data = UserModelSerializer(user).data"""
        payload = str("<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:aut=\"http://www.mop.cl/controlextraccion/xsd/datosExtraccion/AuthSendDataExtraccionRequest\">\n<soapenv:Header>\n<aut:authSendDataExtraccionTraza>\n<aut:codigoDeLaObra>{codigo_obra}</aut:codigoDeLaObra>\n<aut:timeStampOrigen>{time_stamp_origen}</aut:timeStampOrigen>\n</aut:authSendDataExtraccionTraza>\n</soapenv:Header>\n<soapenv:Body>\n<aut:authSendDataExtraccionRequest>\n<aut:authDataUsuario>\n<aut:idUsuario>\n<aut:rut>{rut}</aut:rut>\n</aut:idUsuario>\n<aut:password>{password}</aut:password>\n</aut:authDataUsuario>\n<!--Optional:-->\n<aut:authDataExtraccionSubterranea>\n<aut:fechaMedicion>{fecha_medicion}</aut:fechaMedicion>\n<aut:horaMedicion>{hora_medicion}</aut:horaMedicion>\n<aut:totalizador>{totalizador}</aut:totalizador>\n<aut:caudal>{caudal}</aut:caudal>\n<aut:nivelFreaticoDelPozo>{nivel_freatico_del_pozo}</aut:nivelFreaticoDelPozo>\n</aut:authDataExtraccionSubterranea>\n</aut:authSendDataExtraccionRequest>\n</soapenv:Body>\n</soapenv:Envelope>").format(totalizador=int(0),
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              rut=rut,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              password=password,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              caudal=float(
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  0),
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              nivel_freatico_del_pozo=float(
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  18.0),
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              codigo_obra=codigo_obra,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              time_stamp_origen="2023-11-11T09:00:00-03:00",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              fecha_medicion="2023-11-11",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              hora_medicion="00:00")

        headers = {
            'Content-Type': 'application/xml'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return Response(response.text, status=status.HTTP_201_CREATED)


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

    xlsx_ignore_headers = ['modified', 'id',
                           'date_time_medition', 'profile_client']
    column_header = {
        'titles': [
            "FECHA",
            "CAUDAL",
            "ACUMULADO",
            "NIVEL"
        ]
    }
