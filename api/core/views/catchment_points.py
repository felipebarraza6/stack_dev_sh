"""Catchment Points views."""
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from api.core.serializers import (
    ClientSerializer,
    ProjectCatchmentsSerializer,
    CatchmentPointSerializer,
    ProfileIkoluCatchmentSerializer,
    NotificationsCatchmentSerializer,
    ResponseNotificationsCatchmentSerializer,
    TypeFileCatchmentSerializer,
    FileCatchmentSerializer,
    CatchmentPointIkoluSerializer,
    ProfileDataConfigCatchmentSerializer,
    ResponseDepthNotificationsCatchmentSerializer,
    DgaDataConfigCatchmentSerializer,
    SchemesCatchmentSerializer,
    VariableSerializer,
    RegisterPersonsSerializer,
    CatchmentPointSerializerDetailCron

)
from api.core.models.catchment_points import (
    Client,
    ProjectCatchments,
    CatchmentPoint,
    ProfileIkoluCatchment,
    NotificationsCatchment,
    ResponseNotificationsCatchment,
    TypeFileCatchment,
    FileCatchment,
    ProfileDataConfigCatchment,
    DgaDataConfigCatchment,
    SchemesCatchment,
    Variable,
    RegisterPersons
)


class ClientViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = "id"


class ProjectCatchmentsViewSet(mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = ProjectCatchments.objects.all()
    serializer_class = ProjectCatchmentsSerializer
    lookup_field = "id"


class CatchmentPointViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = CatchmentPoint.objects.all()
    serializer_class = CatchmentPointSerializer
    lookup_field = "id"

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return CatchmentPointIkoluSerializer 
        elif self.action in ['list']:
            return CatchmentPointSerializer        
        return CatchmentPointSerializer 
    


class ProfileIkoluCatchmentViewSet(mixins.CreateModelMixin,
                                   mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.ListModelMixin,
                                   mixins.DestroyModelMixin,
                                   viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = ProfileIkoluCatchment.objects.all()
    serializer_class = ProfileIkoluCatchmentSerializer
    lookup_field = "id"


class NotificationsCatchmentViewSet(mixins.CreateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.DestroyModelMixin,
                                    viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = NotificationsCatchment.objects.all().order_by('-created')
    serializer_class = NotificationsCatchmentSerializer
    lookup_field = "id"

    class FilterNotificationsCatchment(filters.FilterSet):
        class Meta:
            model = NotificationsCatchment
            fields = {
                'point_catchment': ['exact'],
                'type_variable': ['exact'],
                'type_notification': ['exact'],
                'type_alert': ['exact'],
                'is_periodic': ['exact'],
                'is_active': ['exact'],
                'is_read': ['exact'],
                'is_response': ['exact'],
                'is_finish': ['exact'],
                'is_wait': ['exact'],
                'start_date': ['exact'],
                'end_date': ['exact'],
                
            }
            
    filterset_class = FilterNotificationsCatchment


class ResponseNotificationsCatchmentViewSet(mixins.CreateModelMixin,
                                            mixins.RetrieveModelMixin,
                                            mixins.UpdateModelMixin,
                                            mixins.ListModelMixin,
                                            mixins.DestroyModelMixin,
                                            viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = ResponseNotificationsCatchment.objects.all().order_by('-created')
    serializer_class = ResponseNotificationsCatchmentSerializer
    lookup_field = "id"

    class FilterNotificationsCatchment(filters.FilterSet):
        class Meta:
            model = ResponseNotificationsCatchment
            fields = {
                'notification': ['exact'],
                'user': ['exact']
                
            }
    
    def get_serializer_class(self):
        if self.action in ['list']:
            return ResponseDepthNotificationsCatchmentSerializer
        return ResponseNotificationsCatchmentSerializer
            
    filterset_class = FilterNotificationsCatchment


class TypeFileCatchmentViewSet(mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = TypeFileCatchment.objects.all()
    serializer_class = TypeFileCatchmentSerializer
    lookup_field = "id"


class FileCatchmentViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.ListModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = FileCatchment.objects.all()
    serializer_class = FileCatchmentSerializer
    lookup_field = "id"


class ProfileDataConfigCatchmentViewSet(mixins.CreateModelMixin,
                                        mixins.RetrieveModelMixin,
                                        mixins.UpdateModelMixin,
                                        mixins.ListModelMixin,
                                        mixins.DestroyModelMixin,
                                        viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = ProfileDataConfigCatchment.objects.all()
    serializer_class = ProfileDataConfigCatchmentSerializer
    lookup_field = "id"


class DgaDataConfigCatchmentViewSet(mixins.CreateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.DestroyModelMixin,
                                    viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = DgaDataConfigCatchment.objects.all()
    serializer_class = DgaDataConfigCatchmentSerializer
    lookup_field = "id"


class SchemesCatchmentViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = SchemesCatchment.objects.all()
    serializer_class = SchemesCatchmentSerializer
    lookup_field = "id"


class VariableViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = Variable.objects.all()
    serializer_class = VariableSerializer
    lookup_field = "id"


class RegisterPersonsViewSet(mixins.CreateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.ListModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = RegisterPersons.objects.all()
    serializer_class = RegisterPersonsSerializer
    lookup_field = "id"
