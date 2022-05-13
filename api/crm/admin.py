

# Django
from django.contrib import admin

# Models
from api.crm.models import (InteractionDetail, User, 
                        Client, Action, ProfileClient,
                        RegisterPersons, DataHistoryFact,
                        AdminView)


admin.site.register(ProfileClient)
admin.site.register(RegisterPersons)
admin.site.register(DataHistoryFact)
admin.site.register(AdminView)
admin.site.register(InteractionDetail)
admin.site.register(User)
admin.site.register(Client)
