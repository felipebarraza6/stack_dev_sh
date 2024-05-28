"""Propiedades principales de almacenamiento."""
from django.db import models
from .utils import ModelApi
from .client_profile import ProfileClient


class InteractionDetail(ModelApi):
    """Mode de almacenamiento."""
    profile_client = models.ForeignKey(ProfileClient, blank=True, null=True,
        on_delete=models.CASCADE)
    flow = models.CharField(max_length=400, blank=True, null=True)
    date_time_medition = models.DateTimeField(max_length=800, blank=True, null=True)
    total = models.CharField(max_length=400, blank=True, null=True)
    nivel = models.CharField(max_length=400, blank=True, null=True)
    is_send_dga = models.BooleanField(default=False)
    soap_return = models.TextField(max_length=3000, blank=True, null=True)

    def __str__(self):
        return str(self.profile_client)
