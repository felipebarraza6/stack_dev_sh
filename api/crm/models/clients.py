# Django
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

# Utils
from .utils import ModelApi


class Client(ModelApi):
	
	# General
	phone_regex = RegexValidator(
		regex=r'\+?1?\d{9,15}$',
		message="El número de telefono debe ingresarse en el formato: +9999999. Se permiten hasta 15 dígitos."
	)

	type_client = models.CharField(max_length=40, blank=True, null=True)
	name = models.CharField(max_length=20, null = False, blank= False)
	rut = models.CharField(max_length=10, null=True, blank=True)
	region = models.CharField(max_length=120, null=True, blank=True)
	province = models.CharField(max_length=20, null=True, blank=True)
	commune = models.CharField(max_length=20, null=True, blank=True)
	address_exact = models.CharField(max_length=60, null=True, blank=True)
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
	email = models.EmailField('email', unique = True,
		error_messages={
			'unique' : "Un cliente(empresa) con ese email ya existe."
		}, null= True, blank = True)	
	# General
	#APR
	administered = models.TextField(choices = [('Comite', 'Comite'), ('Cooperativa', 'Cooperativa')], null=False, blank=True)
	number_starts = models.IntegerField(blank=True, null=True)
	date_jurisdiction = models.DateField(null=True, blank=True)
	#APR
	#ENTERPRISE	
	amount_regularized = models.IntegerField(blank=True, null=True)
	flow_rates = models.CharField(max_length=200, blank=True, null=True)
	category =  models.CharField(max_length=40, blank=True, null=True)
	#ENTERPRISE
	

	is_active = models.BooleanField(
		'is Active',
		default = True
	)

	def __str__(self):
		return self.name


class TechnicalInfo(ModelApi):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    rersolution = models.CharField(max_length=300, blank=True, null=True)
    standar = models.CharField(max_length=300, blank=True, null=True)
    date_instalation = models.DateField(blank=True, null=True)
    date_transmission = models.DateField(blank=True, null=True)
    date_official = models.DateField(blank=True, null=True)


    def __str__(self):
        return str(self.client)


class Employee(ModelApi):
	
	enterprise = models.ForeignKey('Client', on_delete = models.CASCADE)
	name = models.CharField(max_length=50, blank=True, null=True)

	charge = models.TextField(max_length=30, null=True, blank=True)
	
	phone_regex = RegexValidator(
		regex=r'\+?1?\d{9,15}$',
		message="El número de telefono debe ingresarse en el formato: +9999999. Se permiten hasta 15 dígitos."
	)

	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
	email = models.EmailField(
		'email',
		unique = True,
		error_messages={
			'unique' : "Un empelado con ese email ya existe."
		},
		blank=False,
		null=False
	)

	is_active = models.BooleanField(
		'is Active',
		default = True
	)

	def __str__(self):
		return self.name + self.enterprise
