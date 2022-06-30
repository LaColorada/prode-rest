import datetime

from core.models import BaseModel
from django.core.exceptions import ValidationError
from django.db import models


class Match(BaseModel):

    name = models.CharField(max_length=255)
    tournament = models.ForeignKey(
        "prode.Tournament", on_delete=models.CASCADE, blank=True, null=True
    )
    start_date = models.DateTimeField(blank=True, null=True)
    duration_mins = models.IntegerField(default=90)
    match_end = models.BooleanField(default=False)
    team1 = models.ForeignKey(
        "prode.Team", on_delete=models.CASCADE, related_name="team1"
    )
    team2 = models.ForeignKey(
        "prode.Team", on_delete=models.CASCADE, related_name="team2"
    )
    team1_score = models.PositiveIntegerField(default=0)
    team2_score = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.team1 == self.team2:
            raise Exception("Team1 cannot be the same as Team2")
        super(Match, self).save(*args, **kwargs)

    @property
    def finalized(self):
        return datetime.datetime.now() >= (
            self.start_date + datetime.timedelta(minutes=self.duration_mins)
        )
