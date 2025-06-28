"""
Models for the Support application, handling tickets and replies.
"""
from django.db import models
from django.conf import settings
from api.apps.common.models import BaseModel

class Ticket(BaseModel):
    """
    Represents a support ticket, which can be linked to a telemetry point
    or a client project.
    """
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        CLOSED = 'CLOSED', 'Closed'
        RESOLVED = 'RESOLVED', 'Resolved'

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.OPEN)
    
    # Optional image attachment for context
    image = models.ImageField(
        upload_to='support_tickets/', null=True, blank=True)
    
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
        # Using .pk is a robust way to access the primary key
        return f"TICKET-{self.pk}: {self.title}"


class TicketReply(BaseModel):
    """
    Represents a reply to a support ticket.
    """
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()

    # Optional image attachment for context in replies
    image = models.ImageField(
        upload_to='support_replies/', null=True, blank=True)

    class Meta:
        verbose_name = "Ticket Reply"
        verbose_name_plural = "Ticket Replies"
        db_table = 'support_ticket_reply'
        ordering = ['created_at']

    def __str__(self):
        return f"Reply by {self.user} on {self.ticket}" 