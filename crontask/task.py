"""Celery tasks."""

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Celery
from celery.decorators import periodic_task
import logging

# Utilities
from datetime import timedelta
logger = logging.getLogger()


@periodic_task(name='add_interaction', run_every=timedelta(seconds=50))
def prueba():
    """Disable finished rides."""
    logger.warning("AAAAAAAA")