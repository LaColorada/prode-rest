from django.db import models


class Tournament(models.Model):

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"({self.id}) {self.name}"
