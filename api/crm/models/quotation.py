from .utils import ModelApi
from .clients import Client 
from django.db import models
import uuid

class Quotation(ModelApi):
    uuid = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_end = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    
    def __str__(self):
        return str(self.client)


class Well(ModelApi):
    quotation = models.ForeignKey(Quotation, blank=True, null=True,
            on_delete=models.CASCADE)
    granted_flow = models.CharField(max_length=1000, blank=True, null=True)
    well_depth = models.CharField(max_length=1000, blank=True, null=True)
    static_level = models.CharField(max_length=1000, blank=True, null=True) 
    dynamic_level = models.CharField(max_length=1000, blank=True, null=True)
    pump_installation_depth = models.CharField(max_length=1000, blank=True, null=True)
    inside_diameter_well = models.CharField(max_length=1000, blank=True, null=True)
    duct_outside_diameter = models.CharField(max_length=1000, blank=True, null=True)


    def __str__(self):
        return str(self.quotation)


