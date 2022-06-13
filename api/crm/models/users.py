"""User Model."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Utils
from .utils import ModelApi

class User(ModelApi, AbstractUser):

    email = models.EmailField(
        'email address',
        unique = True,
        error_messages={
            'unique': 'El usuario ya existe.'
        }
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_verified = models.BooleanField(
        default = True,
        help_text = 'Se establece en verdadero cuando el usuario ha verificado su dirección de correo electrónico'
    )

    is_admin_view = models.BooleanField(default = False)

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email    


