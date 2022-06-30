from django.db import models
from core.models import BaseModel


class Tournament(BaseModel):

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
