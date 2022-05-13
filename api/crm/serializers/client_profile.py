"""Profile Serializers."""
# Django REST Framework
from rest_framework import serializers

# Models
from api.crm.models import (ProfileClient, RegisterPersons,
                            DataHistoryFact, AdminView)




class RegisterPersons(serializers.ModelSerializer):
    class Meta:
        model = RegisterPersons
        fields = '__all__'

class AdminView(serializers.ModelSerializer):
    class Meta:
        model = AdminView
        fields = '__all__'

class ProfileClient(serializers.ModelSerializer):
    class Meta:
        model = ProfileClient
        fields = '__all__'

class DataHistoryFact(serializers.ModelSerializer):
    profile = ProfileClient()
    class Meta:
        model = DataHistoryFact
        fields = '__all__'



