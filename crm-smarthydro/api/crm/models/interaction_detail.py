from django.db import models
from .utils import ModelAp, ModelApi

class InteractionDetail(ModelApi):
    project_code = models.CharField(max_length=400, blank=True, null=True)
    date_medition = models.DateField(max_length=300, blank=True, null=True)
    measurement_time = models.DurationField(blank=True, null=True)
    flow = models.DecimalField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    nivel = models.DecimalField(blank=True, null=True)

    def __init__(self):
        return str(self.project_code)