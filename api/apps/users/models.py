"""
User models for the API.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.

    It uses the email field as the primary identifier for authentication
    and includes timestamp fields for creation and modification tracking.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    # This field seems for temporary password storage, consider a more secure approach in the future.
    text_password = models.CharField(
        max_length=1200, blank=True, null=True, default='pozos.2023')

    is_verified = models.BooleanField(
        default=True,
        help_text='Set to true when the user has verified their email address.'
    )

    class Meta:
        """Meta options."""
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'auth_user' # Using a standard table name

    def __str__(self):
        return self.email 