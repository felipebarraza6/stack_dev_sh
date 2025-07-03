"""
Señales para la app de Cumplimiento
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from api.apps.compliance.models.configs.compliance_config import ComplianceConfig
from api.apps.compliance.models.data.compliance_data import ComplianceData
from api.apps.compliance.models.logs.compliance_log import ComplianceLog


@receiver(post_save, sender=ComplianceConfig)
def compliance_config_saved(sender, instance, created, **kwargs):
    """Señal cuando se guarda una configuración de cumplimiento"""
    if created:
        # Crear log de configuración
        ComplianceLog.objects.create(
            compliance_config=instance,
            activity_type='CONFIGURED',
            status='SUCCESS',
            details={'action': 'created'}
        )


@receiver(post_save, sender=ComplianceData)
def compliance_data_saved(sender, instance, created, **kwargs):
    """Señal cuando se guarda un dato de cumplimiento"""
    if created:
        # Crear log de datos enviados
        ComplianceLog.objects.create(
            compliance_config=instance.compliance_config,
            activity_type='DATA_SENT',
            status='SUCCESS',
            details={'data_id': instance.id, 'status': instance.status}
        ) 