"""Module providingFunction printing python version."""

from django.db import models
import uuid
from .utils import ModelApi
from .clients import Client, ExternalClient 


class Quotation(ModelApi):
    """Quatation interaction details generals. """
    uuid = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    external_client = models.ForeignKey(ExternalClient, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_external_client = models.BooleanField(default=False)
    is_end = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    
    def __str__(self):
        if self.is_external_client:
            return str(self.external_client)
        else:
            return str(self.client)


class Well(ModelApi):
    quotation = models.ForeignKey(Quotation, blank=True, null=True,
            on_delete=models.CASCADE)
    name = models.CharField(max_length=320, blank=True, null=True)       
    type_captation = models.CharField(max_length=320, blank=True, null=True)
    granted_flow = models.CharField(max_length=1000, blank=True, null=True)
    well_depth = models.CharField(max_length=1000, blank=True, null=True)
    static_level = models.CharField(max_length=1000, blank=True, null=True) 
    dynamic_level = models.CharField(max_length=1000, blank=True, null=True)
    pump_installation_depth = models.CharField(max_length=1000, blank=True, null=True)
    inside_diameter_well = models.CharField(max_length=1000, blank=True, null=True)
    duct_outside_diameter = models.CharField(max_length=1000, blank=True, null=True)


    def __str__(self):
        return str(self.quotation)

class Note(ModelApi):
    well = models.ForeignKey(Well, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(max_length=1200, blank=True, null=True)
    img_add = models.ImageField(upload_to='upload/notes/% Y/% m/% d/', blank=True, null=True)


    def __str__(self):
        return str(self.well)


