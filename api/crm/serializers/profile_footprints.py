from rest_framework import serializers
from api.crm.models import (ProfileFootprints, ModuleFootprints, 
                            SectionModuleFootprints, 
                            FieldSectionFootprints, 
                            QuestionSection, 
                            OptionsSelectionFieldFootprints,
                            TicketSupport)

from .supports import TicketSupportModelSerializerRetrieve

class QuestionSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSection
        fields = '__all__'


class OptionsSelectionFieldFootprintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionsSelectionFieldFootprints
        fields = '__all__'


class OptionsSelectionFieldFootprintsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionsSelectionFieldFootprints
        fields = '__all__'


class FieldSectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldSectionFootprints
        fields = '__all__'


class FieldSectionFootprintsSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField('get_options_select')

    def get_options_select(self, field):
        qs = OptionsSelectionFieldFootprints.objects.filter(field=field.id).order_by('created')
        serializer = OptionsSelectionFieldFootprintsSerializer(
            instance=qs, many=True)
        data = serializer.data
        return data

    class Meta:
        model = FieldSectionFootprints
        fields = '__all__'



class SectionModuleFootprintsSerializer(serializers.ModelSerializer):
    fields = serializers.SerializerMethodField('get_fields_per')
    questions = serializers.SerializerMethodField('get_questions_per')

    def get_fields_per(self, section):
        qs = FieldSectionFootprints.objects.filter(section=section.id).order_by('created')
        serializer = FieldSectionFootprintsSerializer(instance=qs, many=True)
        data = serializer.data
        return data

    def get_questions_per(self, section):
        qs = QuestionSection.objects.filter(section=section.id)
        serializer = QuestionSectionSerializer(instance=qs, many=True)
        data = serializer.data
        return data


    class Meta:
        model = SectionModuleFootprints
        fields = '__all__'

class ModuleFootprintsSerializer(serializers.ModelSerializer):
    sections = serializers.SerializerMethodField('get_sections')
    tickets = serializers.SerializerMethodField('get_tickets')

    def get_tickets(self, module):
        qs = TicketSupport.objects.filter(footprint_module=module.id) 
        serializer = TicketSupportModelSerializerRetrieve(instance=qs, many=True)
        data = serializer.data 
        return data

    def get_sections(self, module):
        qs = SectionModuleFootprints.objects.filter(module=module.id).order_by('created')
        serializer = SectionModuleFootprintsSerializer(instance=qs, many=True)
        data = serializer.data
        return data

    class Meta:
        model = ModuleFootprints
        fields = '__all__'


class ProfileFootprintsSerializer(serializers.ModelSerializer):
    modules = serializers.SerializerMethodField('get_modules')

    def get_modules(self, profile):    
        qs = ModuleFootprints.objects.filter(profile=profile.id).order_by('created')
        serializer = ModuleFootprintsSerializer(instance=qs, many=True)
        data = serializer.data
        return data        

    class Meta:
        model = ProfileFootprints
        fields = '__all__'

