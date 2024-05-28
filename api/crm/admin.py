

import datetime
import pytz
from django.urls import reverse
# Django
from django.contrib import admin
# Models
from django.utils.safestring import mark_safe
from django.db.models import F, Max
from django.db.models.functions import TruncMonth
from api.crm.models import (InteractionDetail, User, ProfileClient, VariableClient)  
from import_export.admin import ImportExportModelAdmin, ExportActionMixin


class ProfileAdmin(ImportExportModelAdmin):
        
    def get_interactiondetail_count(self, obj):
        last_data = obj.interactiondetail_set.last()
        if last_data is not None:
            return obj.interactiondetail_set.count()

    def get_last_flow(self, obj):
        last_data = obj.interactiondetail_set.last()
        if last_data is not None:
            return last_data.flow

    def get_last_total(self, obj):
        last_data = obj.interactiondetail_set.last()
        if last_data is not None:
            return last_data.total

    def get_last_nivel(self, obj):
        last_data = obj.interactiondetail_set.last()
        if last_data is not None:
            level_position = float(obj.d3)
            nivel = last_data.nivel
            if nivel is not None:
                nivel_float = float(nivel)
                nivel_f = round(level_position - nivel_float,1)
                txt = f"{nivel_float}<br>n.f: {nivel_f}"
                return mark_safe(txt)


    def get_last_date(self, obj):
        last_data = obj.interactiondetail_set.last()
        if last_data is not None:
            date = last_data.date_time_medition
            zona_horaria_chile = pytz.timezone('America/Santiago')
            date_format = date.astimezone(zona_horaria_chile).strftime("%y/%m/%d %H:%M")
            
            return date_format 
    
    def get_name(self, obj):
        name = obj.title
        standard = obj.standard
        if obj.code_dga_site:
            data = obj.code_dga_site
            txt = f"{name}<br>{data}<br>{standard}" 
            return mark_safe(txt)
        else:
            return name


    def get_first_date(self, obj):
        last_data = obj.interactiondetail_set.first()
        if last_data is not None:
            date = last_data.date_time_medition
            zona_horaria_chile = pytz.timezone('America/Santiago')
            date_format = date.astimezone(zona_horaria_chile).strftime("%y/%m/%d %H:%M")
            return date_format 




    def get_variables(self, obj):
        get_variables = VariableClient.objects.filter(profile=obj.id)
        variable_text = "".join(f"{variable.type_variable[0]}: {variable.str_variable}<br>" if variable.type_variable != 'ACUMULADO' else f"{variable.type_variable[0]}: {variable.str_variable} ({variable.counter})<br>" for variable in get_variables)
        return mark_safe(variable_text)

    def position_nivel(self, obj):
        return obj.d3

    def scale_pt(self, obj):
        return obj.scale

    def get_name_client(self, obj):
        txt = f"{obj.name_client}<br>{obj.user}<br>clave: {obj.user.txt_password}"
        return mark_safe(txt)


     
        

    get_interactiondetail_count.short_description = 'Registros'
    get_first_date.short_description = 'Primer registro'
    get_last_date.short_description = 'Ultimo registro'
    get_last_flow.short_description = 'Caudal'
    get_last_total.short_description = 'Total'
    get_last_nivel.short_description = 'Nivel'
    get_name.short_description = 'Nombre/DGA/ESTANDAR'
    get_variables.short_description = 'Variables'
    position_nivel.short_description = 'Sensor Nivel'
    scale_pt.short_description = 'Escala'
    get_name_client.short_description = 'Cliente'
    

    list_display = ('id','get_name', 'get_name_client',  'scale_pt', 'position_nivel','get_interactiondetail_count', 'get_first_date','get_last_date', 'get_last_flow', 'get_last_total', 'get_last_nivel', "is_send_dga", "is_prom_flow", "get_variables")
    list_filter = ('is_prom_flow', 'is_thethings', 'is_monitoring','scale' ,'is_send_dga','user' ,'name_client','standard')



admin.site.register(ProfileClient, ProfileAdmin)


@admin.register(User)
class UerAdmin(ImportExportModelAdmin):
    
    list_display = ('id' ,'username', 'email', )

    def save_model(self, request, obj, form, change):
        if obj.password == "pbkdf2" + "*":
            obj.password=obj.password
        else:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)



@admin.register(VariableClient)
class VariableAdmin(ImportExportModelAdmin):
    def get_last_data(self, obj):
        if obj.type_variable =="ACUMULADO":
            get = InteractionDetail.objects.filter(profile_client=obj.profile).last()
            if get:
                date = get.date_time_medition
                zona_horaria_chile = pytz.timezone('America/Santiago')
                date_format = date.astimezone(zona_horaria_chile).strftime("%y/%m/%d %H:%M")
                return f"{get.total} - {date_format}"
        """
        if obj.type_variable =="NIVEL":
            get = InteractionDetail.objects.filter(profile_client=obj.profile).last()
            if get:
                date = get.date_time_medition
                zona_horaria_chile = pytz.timezone('America/Santiago')
                date_format = date.astimezone(zona_horaria_chile).strftime("%y/%m/%d %H:%M")
                sus= round(float(obj.profile.d3) - float(get.nivel), 1)
                txt = f"{get.nivel}(n.f: {sus}) - {date_format} "
                return txt 
        """
        if obj.type_variable =="CAUDAL":
            get = InteractionDetail.objects.filter(profile_client=obj.profile).last()
            if get:
                date = get.date_time_medition
                zona_horaria_chile = pytz.timezone('America/Santiago')
                date_format = date.astimezone(zona_horaria_chile).strftime("%y/%m/%d %H:%M")
                return f"{get.flow} - {date_format}"
    
    get_last_data.short_description = 'Ultimo dato'
   

    list_display = ('profile', 'str_variable', 'type_variable', 'is_other_token', 'get_last_data' )
    list_filter = ('profile', 'type_variable' )


@admin.register(InteractionDetail)
class InteractionDetailAdmin(ImportExportModelAdmin):
    def get_nivel_f(self, obj):
        position = obj.profile_client.d3
        if obj.nivel:
            nivel = obj.nivel
            sustraction = round(float(position)-float(nivel),0)
            return sustraction
        
    get_nivel_f.short_description = 'Nivel freatico(mt)'

    list_display = ('id', 'date_time_medition', 'profile_client', 'flow',
            'total', 'nivel', 'get_nivel_f','is_send_dga')
    list_filter = ('profile_client','date_time_medition', 'is_send_dga')
    search_fields = ('date_time_medition',)

    date_hierarchy = 'date_time_medition'

    def changelist_view(self, request, extra_context=None):
        if 'date_time_medition__hour' not in request.GET and 'date_time_medition__minute' not in request.GET:
            q = request.GET.copy()
            q['date_time_medition__hour__gte'] = '0'
            q['date_time_medition__hour__lte'] = '23'
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super().changelist_view(request, extra_context=extra_context)
