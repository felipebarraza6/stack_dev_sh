"""Profile Serializers."""
# Django REST Framework
import pytz
from rest_framework import serializers
from django.utils import timezone
from .users import UserInfoModelSerializer
import datetime

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

class RetrieveProfileClientSerializer(serializers.ModelSerializer):
    variables = serializers.SerializerMethodField('get_variables')
    user = UserInfoModelSerializer()
    last_data = serializers.SerializerMethodField('get_last_data')
    first_data= serializers.SerializerMethodField('get_first_data')
    day_data= serializers.SerializerMethodField('get_day_data')
    day_send_dga = serializers.SerializerMethodField('get_data_send_dga_today')

    def get_variables(self, profile):
        qs = VariableClient.objects.filter(profile=profile)
        serializer = VariableClientModelSerializer(instance=qs, many=True)
        return serializer.data

    def get_last_data(self, profile):
        qs = InteractionDetail.objects.filter(profile_client=profile).last()
        serializer = InteractionDetailSerializer(instance=qs, many=False)
        return serializer.data

    def get_first_data(self, profile):
        qs = InteractionDetail.objects.filter(profile_client=profile).first()
        serializer = InteractionDetailSerializer(instance=qs, many=False)
        return serializer.data
    
    def get_day_data(self, profile):
        chile_tz = pytz.timezone('America/Santiago')
        today = datetime.datetime.now(chile_tz).date()
        qs = InteractionDetail.objects.filter(profile_client=profile, date_time_medition__date=today).order_by('-date_time_medition')
        serializer = InteractionDetailSerializer(instance=qs, many=True)
        return serializer.data
    
    def get_data_send_dga_today(self, profile):
        today = timezone.now().date()
        qs = InteractionDetail.objects.filter(profile_client=profile, date_time_medition__date=today, is_send_dga=True).order_by('-date_time_medition')
        serializer = InteractionDetailSerializer(instance=qs, many=True)
        return serializer.data


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

class ProfileClientSerializer(serializers.ModelSerializer):
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
