

# Django
from django.contrib import admin

# Models
from django.db.models import F, Max
from django.db.models.functions import TruncMonth
from api.core_app.models import (InteractionDetail, User,
                                 ProfileClient, VariableClient)

from import_export.admin import ImportExportModelAdmin, ExportActionMixin


@admin.register(ProfileClient)
class ProfileAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'title', 'code_dga_site', 'is_monitoring',
                    'is_prom_flow', 'token_service', 'name_client', 'is_send_dga', 'qr_dga')
    list_filter = ('name_client', 'is_prom_flow', 'is_thethings')


@admin.register(User)
class UerAdmin(ImportExportModelAdmin):

    list_display = ('id', 'username', 'email', )

    def save_model(self, request, obj, form, change):
        if obj.password == "pbkdf2" + "*":
            obj.password = obj.password
        else:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


@admin.register(VariableClient)
class VariableAdmin(ImportExportModelAdmin):
    list_display = ('profile', 'str_variable', 'type_variable',
                    'is_other_token', 'token_service')


@admin.register(InteractionDetail)
class InteractionAdmin(ImportExportModelAdmin):
    list_display = ('profile_client', 'date_time_medition',
                    'flow', 'nivel', 'total', )


class MidnightFilter(admin.SimpleListFilter):
    title = 'Midnight'
    parameter_name = 'midnight'
