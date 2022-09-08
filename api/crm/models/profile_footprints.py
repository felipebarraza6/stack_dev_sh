"""Water Footprint."""

from django.db import models
from .utils import ModelApi 
from .clients import Client
from .users import User


class ProfileFootprints(ModelApi):
    """ Footprints final data all. """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, blank=True, null=True)
    # init form
    """
    economic_activity = models.CharField(max_length=500, blank=True,null=True)
    res_1238 = models.BooleanField(default=False)
    size_company = models.CharField(max_length=500, blank=True, null=True)
    # add form
    name_represent_legal = models.CharField(max_length=1200, blank=True, null=True)
    phone_represent_legal = models.CharField(max_length=300, blank=True, null=True)
    mail_represent_legal = models.CharField(max_length=500, blank=True, null=True)
    name_admin_apl_enterprise = models.CharField(max_length=500, blank=True, null=True)
    phone_admin_apl_enterprise = models.CharField(max_length=500, blank=True, null=True)
    mail_admin_apl_enterprise = models.CharField(max_length=500, blank=True, null=True)
    activities_org_extraterritorial = models.CharField(max_length=1500, blank=True, null=True)
    cert_postulation = models.CharField(max_length=500, blank=True, null=True)
    # files add form
    file1 = models.FileField(verbose_name='Inscripción de la empresa en el Registro respectivo con certificado de vigencia emitido dentro de los 60 días previos a la fecha de adhesión.', blank=True, null=True)
    file2 = models.FileField(verbose_name='Copia de la personería del representante legal, con certificado de vigencia emitido dentro de los 60 días previos a la fecha de adhesión, que lo habilita para firmar los documentos del APL.', blank=True, null=True)
    file3 = models.FileField(verbose_name='Copia del RUT de la Empresa.', blank=True, null=True)
    file4 = models.FileField(verbose_name='Copia de la patente municipal de la(s) instalación(es) que se someterá(n) al APL.', blank=True, null=True)
    file5 = models.FileField(verbose_name='Copia del título que lo habilita para usar el inmueble que se someterá al APL.', blank=True, null=True)
    file6 = models.FileField(verbose_name='Copia de la inscripción de dominio con vigencia dentro de los 60 días, de los Derechos de Agua en el Registro de Propiedad de Aguas respectivo.', blank=True, null=True)
    file7 = models.FileField(verbose_name='Certificado de inscripción de los derechos de agua en el Catastro Público de Aguas de la DGA, si correspondier, emitido dentro de los 60 dìas', blank=True, null=True)
    file8 = models.FileField(verbose_name='Certificado de pago de los derechos pecuniarios a la Asociación de Canalistas, si correspondiere.', blank=True, null=True)
    file9 = models.FileField(verbose_name='Título que faculta a la empresa adherente para hacer uso de las aguas, para el caso de que no tenga derechos de agua.', blank=True, null=True)
    file10 = models.FileField(verbose_name='Resoluciones de Calificación Ambiental de las instalaciones que se someterán al APL, en caso de que existan.', blank=True, null=True)
    file11 = models.FileField(verbose_name='Permisos o resoluciones sectoriales vigente de las instalaciones de r la empresa adherente en relación a los recursos hídricos.', blank=True, null=True)
    # law declaration
    file12 = models.FileField(verbose_name='Declaracion Jurada', blank=True, null=True)
    """

    def __str__(self):
        return str(self.client)


class ModuleFootprints(ModelApi):
    profile = models.ForeignKey(ProfileFootprints, on_delete=models.CASCADE)
    name = models.CharField(max_length=1200, blank=True, null=True)
    description = models.TextField(max_length=1200, blank=True, null=True)
    number_module = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class SectionModuleFootprints(ModelApi):
    name = models.CharField(max_length=1200, blank=True, null=True)
    module = models.ForeignKey(ModuleFootprints, on_delete=models.CASCADE)
    description = models.TextField(max_length=1200, blank=True, null=True)
    number_section = models.CharField(max_length=12, blank=True, null=True)
    joined = models.BooleanField(default=False)    
    in_validate = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    feedback = models.TextField(max_length=1200, blank=True, null=True)    

    def __str__(self):
        return str(self.name)


class QuestionSection(ModelApi):
    section = models.ForeignKey(
        SectionModuleFootprints, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1200)
    answer = models.TextField(max_length=1200, blank=True, null=True)

    def __str__(self):
        return str(self.comment)


class FieldSectionFootprints(ModelApi):
    
    TYPES_CHOICES = (
        ("SELECT", "SELECT"),
        ("FILE", "FILE"),
        ("TEXT", "TEXT"),
    )

    section = models.ForeignKey(SectionModuleFootprints, on_delete=models.CASCADE)
    label = models.CharField(max_length=500)
    help_text = models.CharField(max_length=500, blank=True, null=True)
    type = models.CharField(max_length=500, choices=TYPES_CHOICES)
    value = models.CharField(max_length=1800, blank=True, null=True)
    file = models.FileField(blank=True, null=True)

    def __str__(self):
        return str(self.label)    


class OptionsSelectionFieldFootprints(ModelApi):
    field = models.ForeignKey(FieldSectionFootprints, on_delete=models.CASCADE)
    name = models.CharField(max_length=1500)

    def __str__(self):
        return str(self.field)










