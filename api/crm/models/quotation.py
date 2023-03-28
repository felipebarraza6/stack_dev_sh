
from django.db import models
import uuid
from .utils import ModelApi
from .clients import Client, Employee, ExternalClient 


class Quotation(ModelApi):
    """Quatation interaction details generals. """
    uuid = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    external_client = models.ForeignKey(ExternalClient, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_external_client = models.BooleanField(default=False)
    is_end = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    pass_technical_department = models.BooleanField(default=False)

    
    def __str__(self):
        return str(self.uuid)


class Well(ModelApi):
    quotation = models.ForeignKey(Quotation, blank=True, null=True,
            on_delete=models.CASCADE)
    name = models.CharField(max_length=320, blank=True, null=True)       
    type_captation = models.CharField(max_length=320, blank=True, null=True)
    granted_flow = models.FloatField(max_length=1000, blank=True, null=True)
    well_depth = models.FloatField(max_length=1000, blank=True, null=True)
    static_level = models.FloatField(max_length=1000, blank=True, null=True) 
    dynamic_level = models.FloatField(max_length=1000, blank=True, null=True)
    pump_installation_depth = models.FloatField(max_length=1000, blank=True, null=True)
    inside_diameter_well = models.FloatField(max_length=1000, blank=True, null=True)
    duct_outside_diameter = models.FloatField(max_length=1000, blank=True, null=True)
    exact_address = models.TextField(max_length=1200, blank=True, null=True)
    has_flow_sensor = models.CharField(max_length=1200, blank=True, null=True) 
    img1 = models.ImageField(blank=True, null=True, upload_to='quotations/wells')
    img2 = models.ImageField(blank=True, null=True, upload_to='quotations/wells')


    def __str__(self):
        return str(self.quotation)


class Note(ModelApi):
    well = models.ForeignKey(Well, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(max_length=1200, blank=True, null=True)    


    def __str__(self):
        return str(self.well)


