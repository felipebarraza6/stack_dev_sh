from rest_framework import serializers
from api.core.models.catchment_points import (
    Client,
    ProjectCatchments,
    CatchmentPoint,
    ProfileIkoluCatchment,
    NotificationsCatchment,
    ResponseNotificationsCatchment,
    TypeFileCatchment,
    FileCatchment,
    ProfileDataConfigCatchment,
    DgaDataConfigCatchment,
    SchemesCatchment,
    Variable,
    RegisterPersons
)
from api.core.models.interaction_detail import InteractionDetail
from datetime import datetime, timedelta
from .interaction_detail import InteractionDetailModelSerializerNoProcessing, InteractionDetailModelSerializer
from django.db.models import Case, When, IntegerField


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ProjectCatchmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCatchments
        fields = '__all__'


class CatchmentPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatchmentPoint
        fields = '__all__'


class ProfileIkoluCatchmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileIkoluCatchment
        fields = '__all__'


class NotificationsCatchmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationsCatchment
        fields = '__all__'


class ResponseDepthNotificationsCatchmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseNotificationsCatchment
        fields = '__all__'
        depth=1

class ResponseNotificationsCatchmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseNotificationsCatchment
        fields = '__all__'


class TypeFileCatchmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeFileCatchment
        fields = '__all__'


class FileCatchmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileCatchment
        fields = '__all__'


class ProfileDataConfigCatchmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileDataConfigCatchment
        fields = '__all__'


class DgaCronSerializer(serializers.ModelSerializer):
    class Meta:
        model = DgaDataConfigCatchment
        fields = ('send_dga', 'standard', 'type_dga', 'code_dga', 'flow_granted_dga',
                  'total_granted_dga', 'shac', 'date_start_compliance', 'date_created_code',)


class VariableCronSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable
        fields = ('str_variable', 'type_variable', 'token_service', 'service',
                  'pulses_factor', 'addition', 'convert_to_lt', 'calculate_nivel',)


class SchemesCatchmentCronSerializer(serializers.ModelSerializer):
    """
    Serializer for SchemesCatchment with variables.
    """
    variables = serializers.SerializerMethodField()

    def get_variables(self, obj):
        """
        Retrieve and serialize variables for the given scheme catchment.
        """
        get_data = Variable.objects.filter(
            scheme_catchment=obj).all().order_by(
            Case(
                When(type_variable='TOTALIZADO', then=0),
                When(token_service__isnull=True, then=2),
                default=1,
                output_field=IntegerField()
            ),
            'type_variable',
            'token_service'
        )
        return VariableCronSerializer(get_data, many=True).data

    class Meta:
        model = SchemesCatchment
        fields = ('name', 'variables')


class ProfileDataConfigCatchmentRetrieveCronSerializer(serializers.ModelSerializer):
    scheme = serializers.SerializerMethodField('get_scheme')

    def get_scheme(self, obj):
        get_data = SchemesCatchment.objects.filter(
            points_catchment=obj.point_catchment).first()
        return SchemesCatchmentCronSerializer(get_data).data

    class Meta:
        model = ProfileDataConfigCatchment
        fields = ('token_service', "d3", 'scheme',)


class DgaDataConfigCatchmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DgaDataConfigCatchment
        fields = '__all__'


class SchemesCatchmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemesCatchment
        fields = '__all__'


class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable
        fields = '__all__'


class RegisterPersonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterPersons
        fields = '__all__'


class ProfileIkoluCatchmentRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileIkoluCatchment
        fields = ('entry_by_form', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6')


class DataConfigUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileDataConfigCatchment
        fields = ('d1', 'd2', 'd3', 'd4', 'd5','d6',
                  'date_start_telemetry', 'date_delivery_act','is_telemetry')


class InteractionDetailModuleSerializer(serializers.ModelSerializer):
    date_time_medition = serializers.DateTimeField(format="%Y-%d-%m %H:%M")

    class Meta:
        model = InteractionDetail
        fields = ('date_time_medition', 'date_time_last_logger', 'flow', 'total', 'total_diff', 'total_today_diff',
                  'nivel', 'water_table', 'send_dga', 'return_dga', 'n_voucher')


class TypeFileCatchmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeFileCatchment
        fields = ('name',)


class FileCatchmentDetailSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%d-%m %H:%M")
    modified = serializers.DateTimeField(format="%Y-%d-%m %H:%M")
    type_file = serializers.SerializerMethodField('get_type_file')

    def get_type_file(self, obj):
        return TypeFileCatchmentDetailSerializer(obj.type_file).data

    class Meta:
        model = FileCatchment
        fields = ('id', 'file', 'name', 'description',
                  'created', 'modified', 'type_file')


class NotificationsCatchmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationsCatchment
        fields = ('id', 'created', 'title', 'message',
                  'type_variable', 'value', 'type_alert', 'type_notification')


class CatchmentPointIkoluSerializer(serializers.ModelSerializer):
    profile_ikolu = serializers.SerializerMethodField(
        'get_profile_ikolu')
    config_data = serializers.SerializerMethodField(
        'get_config_data')
    dga = serializers.SerializerMethodField(
        'get_dga')
    modules = serializers.SerializerMethodField('get_modules')

    def get_modules(self, obj):
        """
        Obtener módulos activos del punto de captación
        """
        try:
            profile = ProfileIkoluCatchment.objects.filter(
                point_catchment=obj).first()
            
            if profile:
                modules = []
                
                if profile.m1:
                    modules.append({
                        'id': 'm1',
                        'name': 'Mi Pozo',
                        'active': True,
                        'subscription_type': None,
                        'start_date': None
                    })
                
                if profile.m2:
                    modules.append({
                        'id': 'm2',
                        'name': 'DGA',
                        'active': True,
                        'subscription_type': None,
                        'start_date': None
                    })
                
                if profile.m3:
                    modules.append({
                        'id': 'm3',
                        'name': 'Datos y Reportes',
                        'active': True,
                        'subscription_type': profile.m3_type_subscriptions,
                        'start_date': profile.m3_start_subscription
                    })
                
                if profile.m4:
                    modules.append({
                        'id': 'm4',
                        'name': 'Gráficos',
                        'active': True,
                        'subscription_type': profile.m4_type_subscriptions,
                        'start_date': profile.m4_start_subscription
                    })
                
                if profile.m5:
                    modules.append({
                        'id': 'm5',
                        'name': 'Indicadores',
                        'active': True,
                        'subscription_type': profile.m5_type_subscriptions,
                        'start_date': profile.m5_start_subscription
                    })
                
                if profile.m6:
                    modules.append({
                        'id': 'm6',
                        'name': 'Alarmas',
                        'active': True,
                        'subscription_type': profile.m6_type_subscriptions,
                        'start_date': profile.m6_start_subscription
                    })
                
                if profile.m7:
                    modules.append({
                        'id': 'm7',
                        'name': 'Documentos',
                        'active': True,
                        'subscription_type': profile.m7_type_subscriptions,
                        'start_date': profile.m7_start_subscription
                    })
                
                return modules
            
            return []
            
        except Exception as e:
            return []

    def get_dga(self, obj):
        """
        Obtener configuración DGA del punto
        """
        try:
            dga_config = DgaDataConfigCatchment.objects.filter(
                point_catchment=obj).first()
            
            if dga_config:
                return {
                    'send_dga': dga_config.send_dga,
                    'standard': dga_config.standard,
                    'type_dga': dga_config.type_dga,
                    'code_dga': dga_config.code_dga,
                    'flow_granted_dga': dga_config.flow_granted_dga,
                    'total_granted_dga': dga_config.total_granted_dga,
                    'shac': dga_config.shac,
                    'date_start_compliance': dga_config.date_start_compliance,
                    'date_created_code': dga_config.date_created_code,
                    'name_informant': dga_config.name_informant,
                    'rut_report_dga': dga_config.rut_report_dga
                }
            
            return None
            
        except Exception as e:
            return None

    def get_config_data(self, obj):
        """
        Obtener configuración de datos del punto
        """
        try:
            config = ProfileDataConfigCatchment.objects.filter(
                point_catchment=obj).first()
            
            if config:
                return {
                    'd1': config.d1,
                    'd2': config.d2,
                    'd3': config.d3,
                    'd4': config.d4,
                    'd5': config.d5,
                    'd6': config.d6,
                    'is_telemetry': config.is_telemetry,
                    'date_start_telemetry': config.date_start_telemetry,
                    'date_delivery_act': config.date_delivery_act
                }
            
            return None
            
        except Exception as e:
            return None

    def get_profile_ikolu(self, obj):
        """
        Obtener perfil Ikolu del punto
        """
        try:
            profile = ProfileIkoluCatchment.objects.filter(
                point_catchment=obj).first()
            
            if profile:
                return ProfileIkoluCatchmentRetrieveSerializer(profile).data
            
            return None
            
        except Exception as e:
            return None

    class Meta:
        model = CatchmentPoint
        fields = ('id', 'title','frecuency',
                  'profile_ikolu', 'config_data', 'dga', 'modules')
