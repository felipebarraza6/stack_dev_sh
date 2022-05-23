from django.db import models
from .utils import ModelApi


class InteractionDetail(ModelApi):
    project_code = models.CharField(max_length=400, blank=True, null=True)
    date_medition = models.DateField(max_length=300, blank=True, null=True)
    measurement_time = models.DurationField(blank=True, null=True)
    flow = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    total = models.IntegerField(blank=True, null=True)
    nivel = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.id)