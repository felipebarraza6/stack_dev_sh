from django.db import models
from .utils import ModelApi
from .client_profile import ProfileClient

class InteractionDetail(ModelApi):
    profile_client = models.ForeignKey(ProfileClient, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Punto de captacion")
    date_time_medition = models.DateTimeField(max_length=800, blank=True, null=True, verbose_name="Fecha/hora medicion")
    date_time_last_logger = models.DateTimeField(max_length=800, blank=True, null=True, verbose_name="Fecha/hora logger")    
    flow = models.CharField(max_length=400, blank=True, null=True, verbose_name="Caudal(lt)")
    total = models.CharField(max_length=400, blank=True, null=True, verbose_name="Total(m3)")
    nivel = models.CharField(max_length=400, blank=True, null=True, verbose_name="Nivel(mt)")
    is_send_dga = models.BooleanField(default=False, verbose_name="DGA")
    soap_return = models.TextField(max_length=3000, blank=True, null=True)

    class Meta:
        verbose_name = 'Registro telemetria'
        verbose_name_plural = 'Registros Telemetria'

    

    def __str__(self):
        return str(self.profile_client)
