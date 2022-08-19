"""Webinars Models."""

from django.db import models 
from .utils import ModelApi


class Webinars(ModelApi):
    title = models.CharField(max_length=355, blank=True, null=True)
    subtitule = models.CharField(max_length=655, blank=True, null=True)
    organized_by = models.CharField(max_length=655, blank=True, null=True)
    present = models.CharField(max_length=655, blank=True, null=True)
    img_present = models.ImageField(blank=True, null=True)
    date_time_webinar = models.DateTimeField()
    link_meet = models.CharField(max_length=3000, blank=True, null=True)
    
    def __str__(self):
        return str(self.title)

class ElementsProgramation(ModelApi):
    prefix = models.CharField(max_length=10)
    name = models.CharField(max_length=655, blank=True, null=True)
    webinar = models.ForeignKey(Webinars, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.name)



