"""Profile Serializers."""
# Django REST Framework
from rest_framework import serializers
from .users import UserInfoModelSerializer

# Models
from api.core_app.models import (
    ProfileClient,
    RegisterPersons,
    VariableClient,
    DataHistoryFact,
    InteractionDetail,
)


class RegisterPersons(serializers.ModelSerializer):
    class Meta:
        model = RegisterPersons
        fields = "__all__"


class VariableClientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariableClient
        fields = "__all__"


class RetrieveProfileClientSerializer(serializers.ModelSerializer):
    variables = serializers.SerializerMethodField('get_variables')
    user = UserInfoModelSerializer()
    last_data = serializers.SerializerMethodField('get_last_data')

    def get_variables(self, profile):
        qs = VariableClient.objects.filter(profile=profile)
        serializer = VariableClientModelSerializer(instance=qs, many=True)
        return serializer.data

    def get_last_data(self, profile):
        qs = InteractionDetail.objects.filter(profile_client=profile).first()
        serializer = InteractionDetailSerializer(instance=qs, many=False)
        return serializer.data

    class Meta:
        model = ProfileClient
        fields = "__all__"


class ProfileClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileClient
        fields = "__all__"


class CronProfileClientSerializer(serializers.ModelSerializer):
    variables = serializers.SerializerMethodField('get_variables')

    def get_variables(self, profile):
        qs = VariableClient.objects.filter(profile=profile)
        serializer = VariableClientModelSerializer(instance=qs, many=True)
        return serializer.data

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
