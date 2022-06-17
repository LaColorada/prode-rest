from django.db import models
from django.core.exceptions import ValidationError


# class MatchResult(models.TextChoices):
#         TEAM1_WIN = "TEAM1 WIN"
#         TEAM2_WIN = "TEAM2 WIN"
#         DRAW = "DRAW"


class Match(models.Model):

    name = models.CharField(max_length=255)
    team1 = models.ForeignKey(
        "prode.Team", on_delete=models.CASCADE, related_name="team1"
    )
    team2 = models.ForeignKey(
        "prode.Team", on_delete=models.CASCADE, related_name="team2"
    )
    team1_score = models.PositiveIntegerField(default=0)
    team2_score = models.PositiveIntegerField(default=0)

    # def result(self):
    #     if self.team1_score > self.team2_score:
    #         return MatchResult.TEAM1_WIN
    #     elif self.team2_score > self.team1_score:
    #         return MatchResult.TEAM2_WIN
    #     else:
    #         return MatchResult.DRAW

    def __str__(self):
        return f"({self.id}) {self.name}"

    def clean(self):
        if self.team1 == self.team2:
            raise ValidationError("Teams must be different.")
