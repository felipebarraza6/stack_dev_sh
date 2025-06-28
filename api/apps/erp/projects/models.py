"""
ERP models related to clients and projects.
"""
from django.db import models
from api.apps.common.models import BaseModel

class Client(BaseModel):
    """Represents a client of the company."""
    name = models.CharField(max_length=300)
    identifier = models.CharField(
        max_length=50, unique=True, help_text="RUT or other national identifier.")
    address = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=300, blank=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        db_table = 'erp_client'

    def __str__(self):
        return self.name


class Project(BaseModel):
    """
    Represents a project for a client, which groups a set of
    catchment points.
    """
    name = models.CharField(max_length=300)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='projects')
    internal_code = models.CharField(max_length=300, blank=True)
    
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        db_table = 'erp_project'

    def __str__(self):
        return self.name 