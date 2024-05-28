from rest_framework import serializers
from api.crm.models import InteractionDetail


class InteractionDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteractionDetail
        fields = '__all__'
