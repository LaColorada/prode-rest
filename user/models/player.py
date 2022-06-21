from django.db import models

from django.conf import settings


class Player(models.Model):
    """User player model"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()

    def __str__(self):
        """Defines string for model"""
        return str(self.user)

    class Meta:
        """Ordering players depending score"""

        ordering = ["score"]
