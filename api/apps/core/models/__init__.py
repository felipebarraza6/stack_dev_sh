# Importar modelos base para que Django los reconozca
from .base import BaseModel, TimestampedModel, SoftDeleteModel

__all__ = ['BaseModel', 'TimestampedModel', 'SoftDeleteModel'] 