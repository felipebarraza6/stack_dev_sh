

# Django
from django.contrib import admin

# Models
from api.crm.models import (InteractionDetail, User, 
                            ProfileClient, VariableClient)
                        
from import_export.admin import ExportActionMixin

@admin.register(ProfileClient)
class ProfileAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('user', 'title', 'code_dga_site', 'is_monitoring', 'is_prom_flow', 'token_service')

admin.site.register(User)

@admin.register(VariableClient)
class VariableAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('profile', 'str_variable', 'type_variable', 'is_other_token', 'token_service')

@admin.register(InteractionDetail)
class UserAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('id', 'date_time_medition', 'profile_client', 'flow',
            'total', 'nivel', 'is_send_dga')
    list_filter = ('profile_client',)
    date_hierarchy = 'date_time_medition'
