from rest_framework import serializers
from api.crm.models.quotation import Note, Quotation, Well
from api.crm.models.clients import ExternalClient
from .clients import ExternalClientModelSerializer

class NoteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class QuotationsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = '__all__'

class WellsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Well
        fields = '__all__'

class QuotationRetrieveModelSerializer(serializers.ModelSerializer):
    external_client = ExternalClientModelSerializer()
    wells = serializers.SerializerMethodField('get_wells')

    def get_wells(self, quotation):
        qs = Well.objects.filter(quotation_id=quotation.uuid)
        serializer = WellsModelSerializer(instance=qs, many=True)
        data = serializer.data
        return data

    class Meta:
        model = Quotation
        fields = (
            'uuid',
            'client',
            'external_client',
            'wells'
        )


