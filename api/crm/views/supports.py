from rest_framework import mixins, viewsets, status
from django_filters import rest_framework as filters

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

from api.crm.models import SupportSection, TicketSupport, AnswerTicket
from api.crm.serializers import (SupportSectionModelSerializer,
                                TicketSupportModelSerializer,
                                AnswerTicketModelSerializer,
                                AnswerTicketModelSerializerRetrieve,
                                TicketSupportModelSerializerRetrieve) 


class SupportSectionViewSet(mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    ordering = ('created')
    queryset = SupportSection.objects.all()
    serializer_class = SupportSectionModelSerializer

class TicketSupportViewSet(mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    ordering = ('created')
    queryset = TicketSupport.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketSupportModelSerializer
        elif self.action == 'retrieve':
            return TicketSupportModelSerializer
        else:
            return TicketSupportModelSerializer 

class AnswerTicketViewSet(mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    ordering = ('-created')
    queryset = AnswerTicket.objects.all()
    serializer_class = AnswerTicketModelSerializer 

