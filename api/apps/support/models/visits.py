"""
Model for scheduling and tracking field visits related to support tickets.
"""
from django.db import models
from django.conf import settings
from api.apps.common.models import BaseModel

class FieldVisit(BaseModel):
    """
    Represents a scheduled field visit by a technician for a specific support ticket.
    """
    class Status(models.TextChoices):
        SCHEDULED = 'SCHEDULED', 'Scheduled'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    ticket = models.ForeignKey(
        'support.Ticket', on_delete=models.CASCADE, related_name='field_visits')
    
    technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='field_assignments'
    )
    
    scheduled_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    
    visit_report = models.TextField(
        null=True, blank=True, help_text="Notes and summary from the technician after the visit.")

    class Meta:
        verbose_name = "Field Visit"
        verbose_name_plural = "Field Visits"
        db_table = 'support_field_visit'
        ordering = ['-scheduled_date', 'start_time']

    def __str__(self):
        technician_name = getattr(self.technician, 'username', 'N/A')
        return f"Visit for TICKET-{self.ticket.pk} on {self.scheduled_date} by {technician_name}" 