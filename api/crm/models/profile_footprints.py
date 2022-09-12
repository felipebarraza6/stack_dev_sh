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
    title_presentation = models.CharField(max_length=200, blank=True, null=True)
    description_presentation = models.TextField(max_length=200, blank=True, null=True)


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










