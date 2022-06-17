from django.db import models
from django.contrib.auth import get_user_model


class Player(models.Model):
    """User player model

    Returns:
        obj: Forecast
    """

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    score = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.first_name} + {self.user.last_name}"
