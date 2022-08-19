

# Django
from django.contrib import admin

# Models
from api.crm.models import (InteractionDetail, User, 
                        Client, Action, ProfileClient,
                        RegisterPersons, DataHistoryFact,
                        TechnicalInfo, Quotation, Well,
                        FormLandingContact, ProfileFootprints, Webinars, ElementsProgramation)
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
admin.site.register(ProfileFootprints)
admin.site.register(Webinars)
admin.site.register(ElementsProgramation)

@admin.register(InteractionDetail)
class UserAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('id', 'date_time_medition', 'profile_client', 'flow',
            'total', 'nivel')
