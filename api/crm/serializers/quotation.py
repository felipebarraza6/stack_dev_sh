from rest_framework import serializers
from api.crm.models.quotation import Quotation, Well


class QuotationsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = '__all__'


class WellsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Well
        fields = '__all__'
