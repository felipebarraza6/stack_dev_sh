from rest_framework import serializers
from api.crm.models import FormLandingContact


class FormLandingContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormLandingContact
        fields = '__all__'
