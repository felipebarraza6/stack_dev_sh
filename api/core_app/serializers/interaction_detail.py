from rest_framework import serializers
from api.core_app.models import InteractionDetail


class InteractionDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteractionDetail
        fields = '__all__'
