"""
Telemetry models related to physical points and data entries.
"""
from django.contrib.gis.db import models as gis_models
from django.db import models
from decimal import Decimal

from api.apps.common.models import BaseModel

class CatchmentPoint(BaseModel):
    """
    Represents a physical monitoring point. This is the central model
    for all telemetry data.
    """
    project = models.ForeignKey(
        'erp.Project', related_name='catchment_points',
        on_delete=models.CASCADE, verbose_name='Project')
    
    name = models.CharField(max_length=200, blank=True, null=True)
    
    owner = models.ForeignKey(
        'users.User', related_name='owned_catchment_points', on_delete=models.CASCADE)
    
    viewers = models.ManyToManyField(
        'users.User', related_name="viewed_catchment_points", blank=True)

    # Geographic coordinates
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    location = gis_models.PointField(null=True, blank=True, verbose_name='Location')
    
    # Collection frequency
    class Frequency(models.TextChoices):
        ONE_MINUTE = '1', '1 minute'
        FIVE_MINUTES = '5', '5 minutes'
        SIXTY_MINUTES = '60', '60 minutes'

    frequency = models.CharField(
        max_length=10, choices=Frequency.choices, default=Frequency.SIXTY_MINUTES)
    
    is_telemetry_active = models.BooleanField(default=False)
    telemetry_start_date = models.DateField(null=True, blank=True)
    
    extra_attributes = models.JSONField(default=dict, blank=True, null=True, 
                                        help_text="Flexible field for additional, non-structured data.")

    class Meta:
        verbose_name = "Catchment Point"
        verbose_name_plural = "Catchment Points"
        db_table = 'telemetry_catchment_point'
        indexes = [
            models.Index(fields=['is_telemetry_active']),
            models.Index(fields=['frequency', 'is_telemetry_active']),
        ]

    def __str__(self):
        return f"{self.name} - {self.owner.email}"

class InteractionDetail(BaseModel):
    """
    Stores the raw telemetry data received from providers for a specific
    catchment point.
    """
    catchment_point = models.ForeignKey(
        CatchmentPoint, related_name='interaction_details', on_delete=models.CASCADE,
        blank=True, null=True)
    
    # Processed, standard data
    flow = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal("0.0"))
    level = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal("0.0"))
    volume = models.DecimalField(max_digits=12, decimal_places=3, default=Decimal("0.0"))
    
    # Raw data and metadata
    provider = models.CharField(max_length=50, blank=True, null=True)
    raw_data = models.JSONField(blank=True, null=True, help_text="Raw, unprocessed data from the provider.")
    days_since_last_connection = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Interaction Detail"
        verbose_name_plural = "Interaction Details"
        db_table = 'telemetry_interaction_detail'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['catchment_point', '-created_at']),
            models.Index(fields=['provider', 'created_at']),
        ]

    def __str__(self):
        return f"Data for {self.catchment_point} at {self.created_at}" 