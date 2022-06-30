from django.db import models
import datetime


class BaseModel(models.Model):
    """
    Abstract base class for models
    """

    created_at = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name="created_at"
    )
    updated_at = models.DateTimeField(
        auto_now=True, null=True, verbose_name="updated_at"
    )

    class Meta:
        abstract = True

    def __str__(self):
        object_name = self.__class__.__name__
        if hasattr(self, "name"):
            object_name = self.name
        return f"({self.id}) ({object_name})"
