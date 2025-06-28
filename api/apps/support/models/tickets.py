"""
Core model for the support application, representing a single case file.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.apps import apps
from api.apps.common.models import BaseModel

class Ticket(BaseModel):
    """
    Represents a support ticket, which acts as a complete "case file".
    """
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        FIELD_VISIT_SCHEDULED = 'FIELD_VISIT_SCHEDULED', 'Field Visit Scheduled'
        CLOSED = 'CLOSED', 'Closed'
        RESOLVED = 'RESOLVED', 'Resolved'

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=30, choices=Status.choices, default=Status.OPEN)
    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    
    resolution_notes = models.TextField(
        null=True, blank=True, help_text="Summary of how the issue was resolved.")

    image = models.ImageField(
        upload_to='support_tickets/', null=True, blank=True)
    
    department = models.ForeignKey(
        'support.Department',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='tickets'
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tickets'
    )
    
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='assigned_tickets'
    )
    
    catchment_point = models.ForeignKey(
        'telemetry.CatchmentPoint',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    project = models.ForeignKey(
        'erp.Project',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    
    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        db_table = 'support_ticket'
        ordering = ['-created_at']

    def __str__(self):
        return f"TICKET-{self.pk}: {self.title}"

    def get_connection_status(self, offline_threshold_hours=24):
        if not self.catchment_point:
            return {"status": "N/A", "message": "No catchment point linked."}

        TimeSeriesData = apps.get_model('datastore', 'TimeSeriesData')
        
        last_data = TimeSeriesData.objects.filter(
            variable__scheme__point=self.catchment_point
        ).order_by('-timestamp').first()

        if not last_data:
            return {"status": "No Data", "message": "No telemetry data ever received."}

        last_seen_timestamp = getattr(last_data, 'timestamp', None)
        if not last_seen_timestamp:
            return {"status": "Error", "message": "Data point has no timestamp."}

        if (timezone.now() - last_seen_timestamp).total_seconds() / 3600 > offline_threshold_hours:
            status = "Offline"
        else:
            status = "Online"
        
        message = f"Last seen {last_seen_timestamp.strftime('%Y-%m-%d %H:%M')}"
        return {"status": status, "message": message, "last_seen": last_seen_timestamp} 