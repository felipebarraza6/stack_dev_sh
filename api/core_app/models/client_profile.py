"""Client Profile."""

from django.db import models
from .utils import ModelApi
from .users import User


class ProfileClient(ModelApi):
    standards = [
        ('MAYOR', 'mayor'),
        ('MEDIO', 'medio'),
        ('MENOR', 'menor'),
        ('CAUDALES_MUY_PEQUENOS', 'caudales_muy_pequenos'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_client = models.CharField(max_length=1200, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    token_service = models.CharField(max_length=400, blank=True, null=True)
    code_dga_site = models.CharField(max_length=1200, blank=True, null=True)
    flow_granted_dga = models.CharField(max_length=1200, blank=True, null=True)
    shac = models.CharField(max_length=1200, blank=True, null=True)
    d1 = models.CharField(max_length=100, blank=True, null=True)
    d2 = models.CharField(max_length=100, blank=True, null=True)
    d3 = models.CharField(max_length=100, blank=True, null=True)
    d4 = models.CharField(max_length=100, blank=True, null=True)
    d5 = models.CharField(max_length=100, blank=True, null=True)
    d6 = models.CharField(max_length=100, blank=True, null=True)
    scale = models.IntegerField(blank=True, null=True)
    qr_dga = models.ImageField(blank=True, null=True)
    standard = models.CharField(
        max_length=300, blank=True, null=True, choices=standards)
    is_dga = models.BooleanField(default=False)
    is_apr = models.BooleanField(default=False)
    is_monitoring = models.BooleanField(blank=True, null=True)
    is_send_dga = models.BooleanField(blank=True, null=True)
    is_prom_flow = models.BooleanField(default=False)
    date_monitoring = models.DateField(blank=True, null=True)
    date_reporting_dga = models.DateField(blank=True, null=True)
    date_delivery_act = models.DateField(blank=True, null=True)
    is_thethings = models.BooleanField(default=False)
    frecuency = models.IntegerField(blank=True, null=True, default=60)
    rut_report_dga = models.CharField(max_length=1400, default='17352192-8')
    password_dga_software = models.CharField(
        max_length=1400, default='ZSQgCiDg7y')

    class Meta:
        verbose_name = 'Well'

    def __str__(self):
        return str(('{} - {}').format(self.title, self.user))


class VariableClient(ModelApi):
    profile = models.ForeignKey(
        ProfileClient, related_name='variable_profile', on_delete=models.CASCADE)
    str_variable = models.CharField(max_length=400)
    token_service = models.CharField(max_length=400, blank=True, null=True)
    is_other_token = models.BooleanField(default=False)
    is_other_url = models.BooleanField(blank=True, null=True, default=False)

    VARIABLES = [
        ('NIVEL', 'nivel'),
        ('CAUDAL', 'caudal'),
        ('ACUMULADO', 'acumulado'),
    ]

    SERVICES = [
        ('NOVUS', 'novus'),
        ('THETHINGS', 'thethings'),
    ]
    service = models.CharField(
        max_length=1200, choices=SERVICES, blank=True, null=True)
    type_variable = models.CharField(max_length=1200, choices=VARIABLES)
    counter = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return str(self.profile)


class RegisterPersons(ModelApi):
    profile = models.ForeignKey(
        ProfileClient, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, blank=True, null=True)
    email = models.CharField(max_length=300, blank=True, null=True)
    phone = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class DataHistoryFact(ModelApi):
    profile = models.ForeignKey(
        ProfileClient, blank=True, null=True, on_delete=models.CASCADE)
    month = models.CharField(max_length=300, blank=True, null=True)
    production = models.IntegerField(null=True, blank=True)
    billing = models.IntegerField(null=True, blank=True)
    constant_a = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.profile)
