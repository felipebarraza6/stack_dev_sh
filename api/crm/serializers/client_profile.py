"""Profile Serializers."""
# Django REST Framework
from rest_framework import serializers

# Models
from api.crm.models import (
    ProfileClient,
    RegisterPersons,
    DataHistoryFact,
    InteractionDetail,
)


class RegisterPersons(serializers.ModelSerializer):
    class Meta:
        model = RegisterPersons
        fields = "__all__"


class ProfileClient(serializers.ModelSerializer):
    class Meta:
        model = ProfileClient
        fields = "__all__"


class DataHistoryFact(serializers.ModelSerializer):
    profile = ProfileClient()

    class Meta:
        model = DataHistoryFact
        fields = "__all__"


class InteractionDetailSerializer(serializers.ModelSerializer):
    interaction = InteractionDetail()

    class Meta:
        model = InteractionDetail
        fields = "__all__"

    def validate(self, data):
        if not data:
            raise serializers.ValidationError("interaccion invalida")
        return data
