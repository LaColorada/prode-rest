from django.db import models
from django.core.exceptions import ValidationError

import datetime


class Match(models.Model):

    name = models.CharField(max_length=255)
    tournament = models.ForeignKey(
        "prode.Tournament", on_delete=models.CASCADE, blank=True, null=True
    )
    start = models.DateTimeField(blank=True, null=True)  # TODO: start_date
    # duration_mins = models.IntegerField()
    match_end = models.BooleanField(default=False, null=True)
    team1 = models.ForeignKey(
        "prode.Team", on_delete=models.CASCADE, related_name="team1"
    )
    team2 = models.ForeignKey(
        "prode.Team", on_delete=models.CASCADE, related_name="team2"
    )
    team1_score = models.PositiveIntegerField(default=0)
    team2_score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"({self.id}) {self.name}"

    def clean(self):
        if self.team1 == self.team2:
            raise ValidationError("Teams must be different.")

    # @property
    # def finalized(self):
    #   return datetime.datetime.now() >= (self.start_date + datetime.timedelta(minutes=self.duration_mins)

    # def started(self):
    #     if datetime.datetime.now() >= self.start:
    #         self.match_end = True
    #         return self.match_end
