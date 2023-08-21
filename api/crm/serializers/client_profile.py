"""Profile Serializers."""
# Django REST Framework
from rest_framework import serializers

# Models
from api.crm.models import (
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

class ProfileClientSerializer(serializers.ModelSerializer):
    
    variables = serializers.SerializerMethodField('get_variables')
    
    def get_variables(self, profile):
        qs = VariableClient.objects.filter(profile = profile)
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
