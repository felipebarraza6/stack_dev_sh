

# Django
from django.contrib import admin

# Models
from api.crm.models import (InteractionDetail, User, 
                        Client, Action, ProfileClient,
                        RegisterPersons, DataHistoryFact,
                        TechnicalInfo, Quotation, Well,
                        FormLandingContact)
from import_export.admin import ExportActionMixin



admin.site.register(ProfileClient)
admin.site.register(RegisterPersons)
admin.site.register(DataHistoryFact)
admin.site.register(User)
admin.site.register(Client)
admin.site.register(Quotation)
admin.site.register(Well)
admin.site.register(TechnicalInfo)
admin.site.register(FormLandingContact)

@admin.register(InteractionDetail)
class UserAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('id', 'date_time_medition', 'profile_client', 'flow',
            'total', 'nivel')
