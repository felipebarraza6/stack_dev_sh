from rest_framework import serializers
from api.crm.models import Webinars, ElementsProgramation


class ElementsProgramationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElementsProgramation
        fields = ('prefix', 'name')


class WebinarsModelSerializer(serializers.ModelSerializer):
    elements = serializers.SerializerMethodField('get_elements')
    
    def get_elements(self, webinar):
        qs = ElementsProgramation.objects.filter(webinar=webinar.id)
        serializer = ElementsProgramationSerializer(instance=qs, many=True)
        data = serializer.data
        return data

    class Meta:
        model = Webinars
        fields = '__all__'


