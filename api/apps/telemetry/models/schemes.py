"""
Telemetry models related to configuration schemes and variables.
"""
from django.db import models
from api.apps.common.models import BaseModel
from .points import CatchmentPoint

class Scheme(BaseModel):
    """
    A template of variables that can be applied to one or more catchment points.
    """
    catchment_points = models.ManyToManyField(
        CatchmentPoint, related_name='schemes', blank=True)
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = "Scheme"
        verbose_name_plural = "Schemes"
        db_table = 'telemetry_scheme'

    def __str__(self):
        return self.name


class Variable(BaseModel):
    """
    A specific telemetry variable that is part of a scheme.
    Defines how to interpret data from a provider.
    """
    scheme = models.ForeignKey(Scheme, related_name='variables', on_delete=models.CASCADE)
    
    class Provider(models.TextChoices):
        NOVUS = 'NOVUS', 'Novus'
        NETTRA = 'NETTRA', 'Nettra'
        TWIN = 'TWIN', 'Twin'

    class VariableType(models.TextChoices):
        LEVEL = 'LEVEL', 'Level'
        FLOW = 'FLOW', 'Flow'
        VOLUME = 'VOLUME', 'Volume'
    
    name = models.CharField(max_length=400, help_text="Internal name or key for the variable.")
    label = models.CharField(max_length=400, help_text="Human-readable label for display.")
    variable_type = models.CharField(max_length=50, choices=VariableType.choices)
    provider = models.CharField(max_length=50, choices=Provider.choices, blank=True, null=True)
    
    # Technical parameters for data processing
    unit = models.CharField(max_length=50, default='m')
    pulse_factor = models.IntegerField(null=True, blank=True, default=1000)
    constant_addition = models.IntegerField(null=True, blank=True, default=0)
    
    extra_attributes = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        verbose_name = "Variable"
        verbose_name_plural = "Variables"
        db_table = 'telemetry_variable'

    def __str__(self):
        return self.name 