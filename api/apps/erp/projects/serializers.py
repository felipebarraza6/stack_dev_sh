"""
Serializers for ERP models related to projects and clients.
"""
from rest_framework import serializers
from api.apps.erp.projects.models import Client, Project

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__' 