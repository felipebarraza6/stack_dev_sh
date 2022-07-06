from django.db import models
from .utils import ModelApi


class FormLandingContact(ModelApi):
    name = models.CharField(max_length=1000, blank=True, null=True)
    phone = models.CharField(max_length=1000, blank=True, null=True)
    email = models.CharField(max_length=1000, blank=True, null=True)
    service = models.CharField(max_length=1000, blank=True, null=True)
    message = models.CharField(max_length=1000, blank=True, null=True)


    def __str__(self):
        return str(self.name)
