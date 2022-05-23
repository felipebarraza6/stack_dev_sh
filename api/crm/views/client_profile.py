from math import perm
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import action
import requests

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
    AdminView as AdminViewM,
    InteractionDetail as Interaction,
)

from api.crm.serializers.client_profile import (
    ProfileClient,
    RegisterPersons,
    DataHistoryFact,
    AdminView,
    InteractionDetailSerializer,
)

list_variables = {
    "nivel": "3grecuc2v",
    "acumulado": "3grecdi1va",
    "caudal": "3grecuc1v",
}
list_productos = {"iansa": "a16508e6-8798-461a-8b07-729e03d8b1ef"}


def get_values(token):
    response = {}
    for item in list_variables.keys():
        parsed_url = (
            f"https://api.tago.io/data/?variable={list_variables[item]}&query=last_item"
        )
        request = requests.get(parsed_url, headers={"authorization": token})
        data = request.json()
        current_time = datetime.strptime(
            data.get("result")[0].get("time"), "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        response["measurement_time"] = datetime.strftime(current_time, "%H:00")
        response["date_medition"] = datetime.strftime(current_time, "%Y-%m-%d")
        if item == "nivel":
            response["nivel"] = data.get("result")[0].get("value")
        elif item == "caudal":
            response["flow"] = data.get("result")[0].get("value")
        else:
            response["total"] = data.get("result")[0].get("value")

    return response


def get_interactions():
    #  obtiene listado de predios
    response = {"data": []}
    for item in list_productos.keys():
        if list_productos[item]:
            data = get_values(list_productos[item])
            data["project_code"] = item
            response["data"].append(data)
    return response


class ClientProfileViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permissions = [AllowAny]
        else:
            permissions = [AllowAny]
        return [p() for p in permissions]

    queryset = ProfileClientM.objects.all()
    serializer_class = ProfileClient
    lookup_field = "id"
    # Filters
    filter_backends = (filters.DjangoFilterBackend,)

    @action(detail=False, methods=["get"])
    def create_interaction(self, request):
        data = get_interactions()
        for item in data.get("data"):
            serializer = InteractionDetailSerializer(data=item)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        # serializer.is_valid(raise_exception=True)
        # user, token = serializer.save()
        # data = {"user": "Hola", "access_token": "qwerty"}
        return Response(data)


class DataHistoryFactViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permissions = [IsAuthenticated]
        else:
            permissions = [AllowAny]
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
