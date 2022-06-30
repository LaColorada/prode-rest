from core.models import BaseModel
from django.conf import settings
from django.db import models


class Player(BaseModel):
    """User player model"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()

    class Meta:
        """Ordering players depending score"""

        ordering = ["score"]

    def __str__(self):
        return f"({self.id}) ({self.user.email})"
