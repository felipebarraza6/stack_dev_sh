from .clients import Client
from .users import User
from django.db import models
from .utils import ModelApi



class Project(ModelApi):
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	name = models.CharField(max_length=600)
	code_internal = models.CharField(max_length=200, blank=True, null=True)
	description = models.TextField(max_length=1200, blank=True, null=True)

	def __str__(self):
		return str(self.id)


class SectionElement(ModelApi):
    name = models.CharField(max_length=1200)
    description = models.CharField(max_length=1200, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class TypeElement(ModelApi):
    section = models.ForeignKey(SectionElement, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=600)
    description = models.TextField(max_length=1200, blank=True, null=True)
    position = models.IntegerField(null=True, blank=True)
    type_file = models.CharField(max_length=1200, blank=True, null=True)
    is_file = models.BooleanField(default=False)
    is_info = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.name)


class ValueElement(ModelApi):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	type_element = models.ForeignKey(TypeElement, on_delete=models.CASCADE)
	name = models.CharField(max_length=600, blank=True, null=True)
	code = models.CharField(max_length=600, blank=True, null=True)
	file = models.FileField(upload_to='files_clients', blank=True, null=True)
	note = models.TextField(max_length=1200, blank=True, null=True)
	is_approved = models.BooleanField(default=False)
	is_read = models.BooleanField(default=False)
	is_cancel = models.BooleanField(default=False)

	def __str__(self):
		return str(self.type_element)


