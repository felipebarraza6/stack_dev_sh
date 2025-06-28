"""Client Profile."""

from django.db import models
from django.core.cache import cache
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from decimal import Decimal
from .utils import ModelApi
from .users import User


class Client(ModelApi):
    """Client Model for Catchment Points."""
    name = models.CharField(max_length=300, verbose_name='Nombre')
    rut = models.CharField(max_length=300, verbose_name='Rut')
    address = models.CharField(max_length=300, verbose_name='Direccion')
    phone = models.CharField(max_length=300, verbose_name='Telefono')
    email = models.CharField(max_length=300, verbose_name='Correo')

    class Meta:
        """Meta data client"""
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f"{self.name}"


class ProjectCatchments(ModelApi):
    """Project Catchments Model."""
    name = models.CharField(max_length=300, verbose_name='Nombre')
    client = models.ForeignKey(
        Client, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Cliente')
    code_internal = models.CharField(
        max_length=300, blank=True, null=True, verbose_name='Codigo interno')

    class Meta:
        """Meta data project catchments"""
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    def __str__(self):
        return f"{self.name}"


class CatchmentPoint(ModelApi):
    """Catchment points model."""
    project = models.ForeignKey(
        ProjectCatchments, related_name='catchment_points',
        on_delete=models.CASCADE, verbose_name='Proyecto')
    title = models.CharField(max_length=200, blank=True,
                             null=True, verbose_name='Nombre')

    owner_user = models.ForeignKey(
        User, related_name='owned_catchment_points', on_delete=models.CASCADE,
        verbose_name='Propietario')
    users_viewers = models.ManyToManyField(
        User, verbose_name='usuario', related_name="viewed_catchment_points", blank=True)

    # Proveedores de telemetría
    is_thethings = models.BooleanField(default=False, verbose_name='Nettra')
    is_tdata = models.BooleanField(default=False, verbose_name="Twin")
    is_novus = models.BooleanField(default=False, verbose_name="Novus")
    
    # Coordenadas geográficas (optimizadas)
    latitude = models.DecimalField(
        max_digits=10, decimal_places=8, null=True, blank=True, verbose_name='Latitud')
    longitude = models.DecimalField(
        max_digits=11, decimal_places=8, null=True, blank=True, verbose_name='Longitud')
    
    # Punto geométrico para consultas espaciales
    location = gis_models.PointField(
        null=True, blank=True, verbose_name='Ubicación')
    
    # Frecuencia de recolección
    FRECUENCY_OPTIONS = [
        ('1', '1 minuto'),
        ('5', '5 minutos'),
        ('60', '60 minutos'),
    ]

    frecuency = models.CharField(
        blank=True, null=True, max_length=300, choices=FRECUENCY_OPTIONS, verbose_name='Frecuencia', default='60')
    
    # Estado de telemetría (optimizado para consultas)
    is_telemetry_active = models.BooleanField(
        default=False, verbose_name='Telemetría activa')
    telemetry_start_date = models.DateField(
        null=True, blank=True, verbose_name='Fecha inicio telemetría')
    
    # Proveedor activo
    active_provider = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Proveedor activo')

    class Meta:
        """Meta data catchment points"""
        verbose_name = 'Punto de captacion'
        verbose_name_plural = 'Puntos de captacion'
        indexes = [
            models.Index(fields=['is_telemetry_active', 'active_provider']),
            models.Index(fields=['frecuency', 'is_telemetry_active']),
            models.Index(fields=['project', 'is_telemetry_active']),
        ]

    def __str__(self):
        return f"{self.title} - {self.owner_user}"
    
    def save(self, *args, **kwargs):
        """Actualizar punto geométrico cuando se cambian coordenadas"""
        if self.latitude and self.longitude:
            self.location = Point(float(self.longitude), float(self.latitude))
        
        super().save(*args, **kwargs)
        
        # Invalidar cache de puntos activos
        cache.delete('active_telemetry_points')
        cache.delete(f'points_frequency_{self.frecuency}')
        if self.active_provider:
            cache.delete(f'points_provider_{self.active_provider}')
    
    @property
    def coordinates(self):
        """Obtener coordenadas como tupla"""
        if self.latitude and self.longitude:
            return (float(self.latitude), float(self.longitude))
        return None
    
    @property
    def is_ready_for_telemetry(self):
        """Verificar si está listo para telemetría"""
        return (
            self.is_telemetry_active and 
            self.active_provider and 
            self.frecuency and
            self.telemetry_start_date
        )
    
    def get_telemetry_config(self):
        """Obtener configuración de telemetría (cacheado)"""
        cache_key = f'telemetry_config_{self.pk}'
        cached_config = cache.get(cache_key)
        
        if cached_config is None:
            # Obtener configuración del perfil de datos
            profile_config = self.data_config_profiles.filter(
                is_telemetry=True
            ).first()
            
            if profile_config:
                config = {
                    'token_service': profile_config.token_service,
                    'frequency': self.frecuency,
                    'provider': self.active_provider,
                    'variables': self._get_variables_config(),
                    'd1': profile_config.d1,
                    'd2': profile_config.d2,
                    'd3': profile_config.d3,
                    'd4': profile_config.d4,
                    'd5': profile_config.d5,
                    'd6': profile_config.d6,
                }
            else:
                config = None
            
            cache.set(cache_key, config, timeout=1800)  # 30 minutos
            cached_config = config
        
        return cached_config
    
    def _get_variables_config(self):
        """Obtener configuración de variables"""
        # TODO: Implementar lógica de variables dinámicas
        return {
            'level': {'enabled': True, 'unit': 'm'},
            'flow': {'enabled': True, 'unit': 'l/s'},
            'total': {'enabled': True, 'unit': 'm3'},
        }


# Funciones de utilidad optimizadas para consultas de telemetría
def get_active_telemetry_points():
    """
    Obtener puntos con telemetría activa (cacheado y optimizado)
    """
    cache_key = 'active_telemetry_points'
    cached_points = cache.get(cache_key)
    
    if cached_points is None:
        # Consulta optimizada con select_related y prefetch_related
        active_points = CatchmentPoint.objects.filter(
            is_telemetry_active=True
        ).select_related(
            'project', 'project__client', 'owner_user'
        ).prefetch_related(
            'data_config_profiles'
        ).only(
            'id', 'title', 'frecuency', 'active_provider',
            'latitude', 'longitude', 'telemetry_start_date',
            'project__name', 'project__client__name',
            'owner_user__username'
        )
        
        cached_points = list(active_points)
        cache.set(cache_key, cached_points, timeout=300)  # 5 minutos
    
    return cached_points


def get_points_by_frequency(frequency):
    """
    Obtener puntos por frecuencia específica (cacheado)
    """
    cache_key = f'points_frequency_{frequency}'
    cached_points = cache.get(cache_key)
    
    if cached_points is None:
        points = CatchmentPoint.objects.filter(
            is_telemetry_active=True,
            frecuency=frequency
        ).select_related('project', 'project__client')
        
        cached_points = list(points)
        cache.set(cache_key, cached_points, timeout=300)  # 5 minutos
    
    return cached_points


def get_points_by_provider(provider):
    """
    Obtener puntos por proveedor específico (cacheado)
    """
    cache_key = f'points_provider_{provider}'
    cached_points = cache.get(cache_key)
    
    if cached_points is None:
        points = CatchmentPoint.objects.filter(
            is_telemetry_active=True,
            active_provider=provider
        ).select_related('project', 'project__client')
        
        cached_points = list(points)
        cache.set(cache_key, cached_points, timeout=300)  # 5 minutos
    
    return cached_points


def get_points_by_project(project_id):
    """
    Obtener puntos por proyecto (cacheado)
    """
    cache_key = f'points_project_{project_id}'
    cached_points = cache.get(cache_key)
    
    if cached_points is None:
        points = CatchmentPoint.objects.filter(
            project_id=project_id,
            is_telemetry_active=True
        ).select_related('project', 'project__client')
        
        cached_points = list(points)
        cache.set(cache_key, cached_points, timeout=300)  # 5 minutos
    
    return cached_points


def invalidate_telemetry_cache():
    """
    Invalidar todos los caches relacionados con telemetría
    """
    cache_keys = [
        'active_telemetry_points',
        'points_frequency_1',
        'points_frequency_5', 
        'points_frequency_60',
        'points_provider_twin',
        'points_provider_nettra',
        'points_provider_novus'
    ]
    
    for key in cache_keys:
        cache.delete(key)


class ProfileIkoluCatchment(ModelApi):
    """Ikolu Status Profile."""

    point_catchment = models.ForeignKey(
        CatchmentPoint, related_name='ikolu_profiles', on_delete=models.CASCADE,
        verbose_name='Punto de captacion')
    entry_by_form = models.BooleanField(
        default=False, verbose_name='Ingreso por formulario')
    m1 = models.BooleanField(
        default=True, verbose_name='MODULO: Mi Pozo')

    m2 = models.BooleanField(default=False, verbose_name='MODULO: DGA')

    SUBSCRIPTIONS_CHOICES = [
        ('MENSUAL', 'mensual'),
        ('TRIMESTRAL', 'trimestral'),
        ('SEMESTRAL', 'semestral'),
        ('ANUAL', 'anual'),
    ]

    m3 = models.BooleanField(
        default=False, verbose_name='MODULO: Datos y reportes')
    m3_start_subscription = models.DateField(
        blank=True, null=True, verbose_name='Fecha inicio suscripción MODULO: Datos y reportes')
    m3_type_subscriptions = models.CharField(
        max_length=300, blank=True, null=True, choices=SUBSCRIPTIONS_CHOICES,
        verbose_name='Tipo de suscripción MODULO: Datos y reportes')

    m4 = models.BooleanField(default=False, verbose_name='MODULO: Graficos')
    m4_start_subscription = models.DateField(
        blank=True, null=True, verbose_name='Fecha inicio suscripción MODULO: Graficos')
    m4_type_subscriptions = models.CharField(
        max_length=300, blank=True, null=True, choices=SUBSCRIPTIONS_CHOICES,
        verbose_name='Tipo de suscripción MODULO: Graficos')

    m5 = models.BooleanField(default=False, verbose_name='MODULO: Indicadores')
    m5_start_subscription = models.DateField(
        blank=True, null=True, verbose_name='Fecha inicio suscripción MODULO: Indicadores')
    m5_type_subscriptions = models.CharField(
        max_length=300, blank=True, null=True, choices=SUBSCRIPTIONS_CHOICES,
        verbose_name='Tipo de suscripción MODULO: Indicadores')

    m6 = models.BooleanField(default=False, verbose_name='MODULO: Alarmas')
    m6_start_subscription = models.DateField(
        blank=True, null=True, verbose_name='Fecha inicio suscripción MODULO: Alarmas')
    m6_type_subscriptions = models.CharField(
        max_length=300, blank=True, null=True, choices=SUBSCRIPTIONS_CHOICES,
        verbose_name='Tipo de suscripción MODULO: Alarmas')

    m7 = models.BooleanField(default=False, verbose_name='MODULO: Documentos')
    m7_start_subscription = models.DateField(
        blank=True, null=True, verbose_name='Fecha inicio suscripción MODULO: Documentos')
    m7_type_subscriptions = models.CharField(
        max_length=300, blank=True, null=True, choices=SUBSCRIPTIONS_CHOICES,
        verbose_name='Tipo de suscripción MODULO: Documentos')

    class Meta:
        """Meta data profile ikolu"""
        verbose_name = 'Perfil Ikolu'
        verbose_name_plural = 'Perfiles Ikolu'

    def __str__(self):
        return f"{self.point_catchment}"


class NotificationsCatchment(ModelApi):
    """Notifications Model."""
    point_catchment = models.ForeignKey(
        CatchmentPoint, related_name='notifications', on_delete=models.CASCADE,
        verbose_name='Punto de captacion')
    title = models.CharField(max_length=300, verbose_name='Titulo')
    message = models.CharField(max_length=1300, verbose_name='Mensaje')
    VARIABLES_CHOICES = [
        ('NIVEL', 'nivel'),
        ('CAUDAL', 'caudal'),
        ('CAUDAL PROMEDIO', 'caudal_promedio((diff/3600)*1000)'),
        ('TOTALIZADO', 'totalizado'), 
        ('TODOS', 'todos')
    ]
    TYPE_NOTIFICATION_CHOICES = [
        ('INFO', 'Informativo'),
        ('WARNING', 'Advertencia'),
        ('ALERT', 'Alerta'),
        ('CRITICAL', 'Crítico'),
        ('SUPPORT', 'Soporte'),
    ]
    TYPE_ALERT_CHOICES = [
        ('MAX', 'mas'),
        ('MIN', 'menos'),
        ('EQUALS', 'igual'),
    ]
    type_variable = models.CharField(
        max_length=300, choices=VARIABLES_CHOICES, verbose_name='Tipo variable', blank=True, null=True)

    value = models.IntegerField(default=0, verbose_name='Valor')
    type_alert = models.CharField(
        max_length=300, choices=TYPE_ALERT_CHOICES, verbose_name='Tipo de alerta', blank=True, null=True)

    type_notification = models.CharField(
        max_length=50, choices=TYPE_NOTIFICATION_CHOICES, verbose_name='Tipo de notificación')

    start_date = models.DateField(
        blank=True, null=True, verbose_name='Fecha inicio')
    end_date = models.DateField(
        blank=True, null=True, verbose_name='Fecha fin')
    
    is_periodic = models.BooleanField(default=False, verbose_name='Cada registro')
    is_active = models.BooleanField(default=True, verbose_name='Activo')

    is_read = models.BooleanField(default=False, verbose_name='Leido')
    is_wait = models.BooleanField(default=False, verbose_name='Espera')
    is_finish = models.BooleanField(default=False, verbose_name='Finalizado')

    class Meta:
        """Meta data notifications"""
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'

    def __str__(self):
        return f"{self.title} - {self.point_catchment}"


class ResponseNotificationsCatchment(ModelApi):
    """Response Notifications Model."""
    notification = models.ForeignKey(
        NotificationsCatchment, related_name='responses',
        on_delete=models.CASCADE, verbose_name='Notificación')
    user = models.ForeignKey(
        User, related_name='responses', on_delete=models.CASCADE, verbose_name='Usuario')
    response = models.CharField(max_length=1300, verbose_name='Respuesta')

    class Meta:
        """Meta data response notifications"""
        verbose_name = 'Respuesta de notificación'
        verbose_name_plural = 'Respuestas de notificaciones'

    def __str__(self):
        return f"{self.notification.title} - {self.user}"


class TypeFileCatchment(ModelApi):
    """Type File Model."""
    name = models.CharField(max_length=300, verbose_name='Nombre')
    internal = models.BooleanField(default=False, verbose_name='Interno')

    class Meta:
        """Meta data type file"""
        verbose_name = 'Tipo de archivo'
        verbose_name_plural = 'Tipos de archivos'

    def __str__(self):
        return f"{self.name}"


class FileCatchment(ModelApi):
    """File Model."""
    point_catchment = models.ForeignKey(
        CatchmentPoint, related_name='files',
        on_delete=models.CASCADE, verbose_name='Punto de captacion')
    type_file = models.ForeignKey(
        TypeFileCatchment, related_name='files',
        on_delete=models.CASCADE, verbose_name='Tipo de archivo')
    name = models.CharField(max_length=300, verbose_name='Nombre')
    file = models.FileField(upload_to='files_catchment',
                            verbose_name='Archivo')
    description = models.CharField(
        max_length=300, verbose_name='Descripción', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        """Meta data file"""
        verbose_name = 'Archivo'
        verbose_name_plural = 'Archivos'

    def __str__(self):
        return f"{self.name} - {self.point_catchment}"


class ProfileDataConfigCatchment(ModelApi):
    """Data Configuration Profile."""
    point_catchment = models.ForeignKey(
        CatchmentPoint, related_name='data_config_profiles',
        on_delete=models.CASCADE, verbose_name='Punto de captacion', blank=True, null=True)
    token_service = models.CharField(max_length=400, blank=True, null=True)
    d1 = models.DecimalField(
        default=Decimal('0.0'), verbose_name='Profundidad(mt)', max_digits=5, decimal_places=2)
    d2 = models.DecimalField(
        default=Decimal('0.0'), verbose_name='Posicionamiento de bomba(mt)', max_digits=5, decimal_places=2)
    d3 = models.DecimalField(
        default=Decimal('0.0'), verbose_name='Posicionamiento nivel(mt)', max_digits=5, decimal_places=2)
    d4 = models.DecimalField(
        default=Decimal('0.0'), verbose_name='Diametro ducto salida bomba(pulg)', max_digits=5, decimal_places=2)
    d5 = models.DecimalField(
        default=Decimal('0.0'), verbose_name='Diametro flujometro(pulg)', max_digits=5, decimal_places=2)
    d6 = models.IntegerField(
        default=0, verbose_name='Caudalimetro inicial', blank=True, null=True)
    is_telemetry = models.BooleanField(
        default=False, verbose_name='Activar telemetría')
    date_start_telemetry = models.DateField(
        blank=True, null=True, verbose_name='Fecha inicio telemetria')
    date_delivery_act = models.DateField(
        blank=True, null=True, verbose_name='Fecha acta de entrega')

    class Meta:
        """Meta data profile data config"""
        verbose_name = 'Configuracion de datos'
        verbose_name_plural = 'Configuracion de datos'

    def __str__(self):
        return f"{self.point_catchment}"


class DgaDataConfigCatchment(ModelApi):
    """Data Configuration Profile DGA."""
    point_catchment = models.ForeignKey(
        CatchmentPoint, related_name='dga_data_config_profiles',
        on_delete=models.CASCADE, verbose_name='Punto de captacion')

    standards_choices = [
        ('SIN_ESTANDAR', 'sin estandar'),
        ('MAYOR', 'mayor'),
        ('MEDIO', 'medio'),
        ('MENOR', 'menor'),
        ('CAUDALES_MUY_PEQUENOS', 'cmp'),
    ]

    types_dga_choices = [
        ('SUBTERRANEO', 'subterraneo'),
        ('SUPERFICIAL', 'superficial'),
    ]

    send_dga = models.BooleanField(
        default=False, verbose_name='Activar cumplimiento')

    standard = models.CharField(
        max_length=300, default='SIN_ESTANDAR', choices=standards_choices, verbose_name='Estandar')
    type_dga = models.CharField(max_length=300, blank=True, null=True,
                                choices=types_dga_choices,
                                default='SUBTERRANEO', verbose_name='Tipo')
    code_dga = models.CharField(
        max_length=1200, blank=True, null=True, verbose_name='Codigo de obra(dga)')
    flow_granted_dga = models.DecimalField(
        max_length=1200, default=Decimal('0.0'), verbose_name='Caudal otorgado(lt/s)', max_digits=5, decimal_places=2)
    total_granted_dga = models.IntegerField(
        blank=True, null=True, verbose_name='Totalizado otorgado(m3)')
    shac = models.CharField(max_length=1200, blank=True,
                            null=True, verbose_name="Sector hidrologico(SHAC)")
    date_start_compliance = models.DateField(
        blank=True, null=True, verbose_name='Fecha inicio envío DGA')
    date_created_code = models.DateField(
        blank=True, null=True, verbose_name='Fecha codigo creacion DGA')
    name_informant = models.CharField(
        max_length=1200, default="Diego Mardones", verbose_name='Nombre informante')
    rut_report_dga = models.CharField(
        max_length=1400, default='17352192-8', verbose_name='RUT')
    password_dga_software = models.CharField(
        max_length=1400, blank=True, null=True, verbose_name='Contraseña software DGA')

    class Meta:
        """Meta data profile data config"""
        verbose_name = 'Configuracion de datos DGA'
        verbose_name_plural = 'Configuraciones de datos DGA'

    def __str__(self):
        return f"{self.point_catchment}"


class SchemesCatchment(ModelApi):
    """Schemes Model."""
    points_catchment = models.ManyToManyField(
        CatchmentPoint, related_name='schemes', verbose_name='Punto de captacion', blank=True)
    name = models.CharField(max_length=300, verbose_name='Nombre')
    description = models.CharField(max_length=300, verbose_name='Descripción')

    class Meta:
        """Meta data schemes"""
        verbose_name = 'Esquema'
        verbose_name_plural = 'Esquemas'

    def __str__(self):
        return f"{self.name}"


class Variable(ModelApi):
    """Variable Model."""
    scheme_catchment = models.ForeignKey(
        SchemesCatchment, related_name='variables',
        on_delete=models.CASCADE, verbose_name='Esquema')

    PROVIDERS_CHOICES = [
        ('NOVUS', 'novus'),
        ('NETTRA', 'nettra'),
        ('TWIN', 'twin'),
    ]
    VARIABLES_CHOICES = [
        ('NIVEL', 'nivel'),
        ('CAUDAL', 'caudal'),
        ('CAUDAL_PROMEDIO', 'caudal_promedio((diff/3600)*1000)'),
        ('TOTALIZADO', 'totalizado')
    ]

    str_variable = models.CharField(
        max_length=400, verbose_name='Variable (str)')
    label = models.CharField(max_length=400, verbose_name='Etiqueta')

    type_variable = models.CharField(
        max_length=1200, choices=VARIABLES_CHOICES, verbose_name='Tipo variable')

    token_service = models.CharField(
        max_length=400, blank=True, null=True, verbose_name='Token')
    service = models.CharField(
        max_length=1200, choices=PROVIDERS_CHOICES, blank=True, null=True, verbose_name='Proveedor')

    # Total
    pulses_factor = models.IntegerField(
        blank=True, null=True, default=1000,
        verbose_name='Pulsos(solo aplica a totalizadores (pulsos*pulsos_factor)/1000)')
    addition = models.IntegerField(
        blank=True, null=True, default=0, verbose_name='Constante(solo aplica a totalizadores)')

    # Caudal
    convert_to_lt = models.BooleanField(
        default=False, verbose_name='Pasar de m3 a lt(solo aplica en caudal) litros/3,6')
    # Nivel
    calculate_nivel = models.IntegerField(
        blank=True, null=True, default=0, verbose_name='Calcular nivel (solo aplica en nivel)')

    class Meta:
        """Meta data variable"""
        verbose_name = 'Variable'
        verbose_name_plural = 'Variables'

    def __str__(self):
        return f"{self.label} - {self.scheme_catchment}"


class RegisterPersons(ModelApi):
    """Register Persons Model."""
    profile = models.ForeignKey(
        ProfileDataConfigCatchment, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, blank=True, null=True)
    email = models.CharField(max_length=300, blank=True, null=True)
    phone = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        """Meta data register persons"""
        verbose_name = 'Persona registrada'
        verbose_name_plural = 'Personas registradas'

    def __str__(self):
        return f"{self.name}"
