"""
Model for organizing support tickets by area of expertise.
"""
from django.db import models
from api.apps.common.models import BaseModel

class Department(BaseModel):
    """
    Represents a team or department within the company, e.g.,
    Software, Hardware, Hydraulics.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        db_table = 'support_department'
        ordering = ['name']

    def __str__(self):
        return self.name 