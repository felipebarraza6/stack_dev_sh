from rest_framework import serializers
from api.crm.models import ProfileFootprints


class ProfileFootprintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileFootprints
        fields = '__all__'
