"""Support Models."""

from .utils import ModelApi
from django.db import models
from .users import User
from .profile_footprints import ModuleFootprints


class SupportSection(ModelApi):
    name = models.CharField(max_length=350)
    description = models.TextField(max_length=1200, blank=True, null=True)

    def __str__(self):
        return self.name


class TicketSupport(ModelApi):
    support_section = models.ForeignKey(SupportSection, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    affair = models.TextField(max_length=1200)
    footprint_module = models.ForeignKey(ModuleFootprints, on_delete=models.CASCADE, blank=True, null=True)
    is_open = models.BooleanField(default=True)
    is_resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user)


class AnswerTicket(ModelApi):
    ticket_support = models.ForeignKey(TicketSupport, on_delete=models.CASCADE)
    administrator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    answer = models.TextField(max_length=1200)
    is_client_answer = models.BooleanField(default=False)
    is_admin_answer = models.BooleanField(default=False)

    def __str__(self):
        return str(self.ticket_support)



