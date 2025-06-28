"""
Models for the Datastore application.

This application is designed to store large volumes of time-series data
efficiently. The models here are optimized for write-heavy workloads,
as they will be primarily used by the high-performance ingestion engine.
"""
from django.db import models
from api.apps.common.models import BaseModel

class TimeSeriesData(BaseModel):
    """
    Stores a single data point for a specific variable at a specific time.
    
    This model uses a flexible JSONField to store the actual value, allowing
    us to accommodate various data types (numeric, text, boolean, etc.)
    without altering the database schema.
    """
    # The variable this data point belongs to.
    variable = models.ForeignKey(
        'telemetry.Variable',
        on_delete=models.CASCADE,
        related_name='time_series_data'
    )
    
    # The timestamp for this data point. Indexed for fast time-based queries.
    timestamp = models.DateTimeField(db_index=True)
    
    # The actual value, stored in a flexible JSON format.
    value = models.JSONField()

    class Meta:
        verbose_name = "Time Series Data"
        verbose_name_plural = "Time Series Data"
        db_table = 'datastore_time_series'
        # Order by most recent data first.
        ordering = ['-timestamp']
        # Create a composite index for faster lookups on variable and time.
        indexes = [
            models.Index(fields=['variable', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.variable.name} at {self.timestamp}: {self.value}" 