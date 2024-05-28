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
    type_dga= [
        ('SUB', 'subterraneo'),
        ('SUP', 'superficial'),
    ]
    module_1 = models.BooleanField(default=True, verbose_name='MODULO: Mi Pozo') 
    module_2 = models.BooleanField(default=False, verbose_name='MODULO: DGA')
    module_3 = models.BooleanField(default=False, verbose_name='MODULO: Datos y reportes')
    module_4 = models.BooleanField(default=False, verbose_name='MODULO: Graficos')
    module_5 = models.BooleanField(default=False, verbose_name='MODULO: Indicadores')
    module_6 = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuario')
    name_client = models.CharField(max_length=1200, blank=True, null=True, verbose_name='Nombre cliente')
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Nombre' )
    token_service = models.CharField(max_length=400, blank=True, null= True)
    code_dga_site = models.CharField(max_length=1200, blank=True, null=True, verbose_name='Codigo de obra(dga)')
    type_dga = models.CharField(max_length=300, blank=True, null= True, choices=type_dga, default='SUB', verbose_name='Captacion')
    flow_granted_dga = models.CharField(max_length=1200, blank=True, null=True, verbose_name='Caudal otorgado') 
    shac = models.CharField(max_length=1200, blank=True, null=True)
    d1 = models.CharField(max_length=100, blank=True, null= True, verbose_name='Profundidad(mt)')
    d2 = models.CharField(max_length=100, blank=True, null= True, verbose_name='Posicionamiento de bomba(mt)')
    d3 = models.CharField(max_length=100, blank=True, null= True,verbose_name='Posicionamiento nivel(mt)' )
    d4 = models.CharField(max_length=100, blank=True, null= True, verbose_name='Diametro ducto salida bomba(pulg)')
    d5 = models.CharField(max_length=100, blank=True, null= True, verbose_name='Diametro flujometro(pulg)')
    d6 = models.CharField(max_length=100, blank=True, null= True)
    scale = models.IntegerField(blank=True, null= True, verbose_name='Escala(lt*pulsos)')
    qr_dga = models.ImageField(blank=True, null=True, verbose_name='QR')
    file_dga = models.FileField(blank=True, null=True, verbose_name='Certificado DGA')
    standard = models.CharField(max_length=300, blank=True, null= True, choices=standards, verbose_name='Estandar') 
    is_dga = models.BooleanField(default=False, verbose_name='Es DGA')
    is_apr = models.BooleanField(default=False, verbose_name='Es APR')    
    is_monitoring = models.BooleanField(blank=True, null=True, verbose_name='Activar monitoreo')
    is_send_dga = models.BooleanField(blank=True, null=True, verbose_name='Envio DGA')
    is_prom_flow = models.BooleanField(default=False, verbose_name='Caudal promedio')
    
    date_reporting_dga = models.DateField(blank=True, null=True, verbose_name='Fecha inicio transmision DGA')
    date_code_dga = models.DateField(blank=True, null=True, verbose_name='Fecha codigo creacion DGA')
    date_report_api = models.DateField(blank=True, null=True, verbose_name='Fecha inicio monitoreo')

    date_delivery_act = models.DateField(blank=True, null=True, verbose_name='Fecha acta de entrega')
    is_thethings = models.BooleanField(default=False, verbose_name='Es Nettra')

    rut_report_dga = models.CharField(max_length=1400, default='17352192-8', verbose_name='RUT')
    password_dga_software = models.CharField(max_length=1400, default='ZSQgCiDg7y', verbose_name='clave DGA') 
    
    class Meta:
        verbose_name = 'Punto de captacion'
        verbose_name_plural = 'Puntos de captacion'

    def __str__(self):
        return str(('{} - {}').format(self.title, self.user))

class VariableClient(ModelApi):
    profile = models.ForeignKey(ProfileClient, related_name='variable_profile', on_delete=models.CASCADE, verbose_name='Punto de captacion')
    str_variable = models.CharField(max_length=400, verbose_name='Variable logger/MQTT')
    token_service = models.CharField(max_length=400, blank=True, null= True, verbose_name='Token de variable')
    is_other_token = models.BooleanField(default=False, verbose_name='Utiliza su propio Token')
    
    is_other_url = models.BooleanField(blank=True, null=True, default=False, verbose_name='Servicio web diferente')
    counter = models.IntegerField(blank=True, null=True, default=0, verbose_name='Contador(solo aplica a totalizadores)')
    
    SERVICES= [
        ('NOVUS', 'novus'),
        ('THETHINGS', 'thethings'),
    ]

    service = models.CharField(max_length=1200, choices=SERVICES, blank=True, null=True, verbose_name='Servicio')

    VARIABLES = [
        ('NIVEL', 'nivel'),
        ('CAUDAL', 'caudal'),
        ('ACUMULADO', 'acumulado'),
    ]

    type_variable = models.CharField(max_length=1200, choices=VARIABLES, verbose_name='Tipo variable')
    convert_to_lt = models.BooleanField(default=False, verbose_name='Pasar a lt(solo aplica en caudal)')

    class Meta:
        verbose_name = 'Variable'
        verbose_name_plural = 'Puntos de captacion - Variables'


    def __str__(self):
        return str(self.profile)

class RegisterPersons(ModelApi):
    profile = models.ForeignKey(ProfileClient, blank=True, null=True, on_delete=models.CASCADE) 
    name = models.CharField(max_length=300, blank=True, null= True)
    email = models.CharField(max_length=300, blank=True, null= True)
    phone = models.CharField(max_length=300, blank=True, null= True)

    def __str__(self):
        return str(self.name)

class DataHistoryFact(ModelApi):
    profile = models.ForeignKey(ProfileClient, blank=True, null=True, on_delete=models.CASCADE)
    month = models.CharField(max_length=300, blank=True, null=True)
    production = models.IntegerField(null=True, blank=True)
    billing = models.IntegerField(null=True, blank=True)
    constant_a = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.profile)



