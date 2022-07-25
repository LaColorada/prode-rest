from core.models import BaseModel
from django.db import models


class Team(BaseModel):

    name = models.CharField(unique=True, max_length=255)
    location = models.CharField(max_length=255)
