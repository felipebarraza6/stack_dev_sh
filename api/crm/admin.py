

# Django
from django.contrib import admin

# Models
from api.crm.models import (InteractionDetail, User, 
                        ExternalClient ,Client, Action, Project, ProfileClient,
                        EconomicActivity, Employee, TypeElement, ValueElement,
                        RegisterPersons, DataHistoryFact,
                        TechnicalInfo, Quotation, Well, Note,
                        FormLandingContact, ProfileFootprints, 
                        Webinars, ElementsProgramation, ModuleFootprints, 
                        SectionModuleFootprints, FieldSectionFootprints, QuestionSection, 
                        OptionsSelectionFieldFootprints, SupportSection,
                        TicketSupport, AnswerTicket, SectionElement)
                        
from import_export.admin import ExportActionMixin

admin.site.register(SupportSection)
admin.site.register(Project)
admin.site.register(TypeElement)
admin.site.register(ValueElement)
admin.site.register(Employee)
admin.site.register(EconomicActivity)
admin.site.register(TicketSupport)
admin.site.register(AnswerTicket)
admin.site.register(OptionsSelectionFieldFootprints)
admin.site.register(ModuleFootprints)
admin.site.register(SectionModuleFootprints)
admin.site.register(FieldSectionFootprints)
admin.site.register(QuestionSection)
admin.site.register(ExternalClient)
admin.site.register(SectionElement)
admin.site.register(Note)
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
