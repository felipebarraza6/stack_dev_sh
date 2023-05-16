# Django
from django.db import models

# Utils
from .utils import ModelApi


class Action(ModelApi):
    type_action = models.ForeignKey('TypeAction', related_name='type_action', on_delete=models.CASCADE)
    client = models.ForeignKey('Client', related_name='client_action', on_delete=models.CASCADE, blank=True, null=True)
    employee = models.ForeignKey('Employee', related_name='employee_action', on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(blank=False, null=False)
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    note = models.TextField(max_length=400, null = False, blank=True)
    is_warning = models.BooleanField(
        'Warning',
        default=False
    )

    is_priority = models.BooleanField(
        'Priority',
        default=False
    )

    is_active = models.BooleanField(
        'Active',
        default = True
    )

    is_complete = models.BooleanField(
        'Complete',
        default = False
    )

    date_complete = models.DateTimeField(blank=True, null=True)


class TypeAction(ModelApi): 
    description = models.CharField(max_length=100, blank=False, null=False)
    is_active = models.BooleanField(
        'Active',
        default = True
    )

    def __str__(self):
        return self.description



