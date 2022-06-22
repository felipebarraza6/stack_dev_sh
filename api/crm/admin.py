

# Django
from django.contrib import admin

# Models
from api.crm.models import (InteractionDetail, User, 
                        Client, Action, ProfileClient,
                        RegisterPersons, DataHistoryFact,
                        AdminView)
from import_export.admin import ExportActionMixin



admin.site.register(ProfileClient)
admin.site.register(RegisterPersons)
admin.site.register(DataHistoryFact)
admin.site.register(AdminView)
admin.site.register(User)
admin.site.register(Client)

@admin.register(InteractionDetail)
class UserAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('id', 'date_time_medition', 'profile_client', 'flow',
            'total', 'nivel')
