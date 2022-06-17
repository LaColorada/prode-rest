from django.db import models


class Forecast(models.Model):
    """Forecast model

    Returns:
        obj: Forecast
    """

    player = models.ForeignKey("prode.Player", on_delete=models.CASCADE)
    match = models.ForeignKey("prode.Match", on_delete=models.CASCADE)
    team1_score = models.PositiveIntegerField()
    team2_score = models.PositiveIntegerField()

    class Meta:
        unique_together = [["player", "match"]]

    def __str__(self):
        return f"({self.id}) {self.match.name}"

    def score(self):
        score = 0
        if None in (
            self.team1_score,
            self.team2_score,
            self.match.team1_score,
            self.match.team2_score,
        ):
            return score
        # SCORE GUESS
        if (
            self.match.team1_score == self.team1_score
            and self.match.team2_score == self.team2_score
        ):
            score += 1
        # DRAW
        if (
            self.match.team1_score == self.match.team2_score
            and self.team1_score == self.team2_score
        ):
            score += 1
        # TEAM1 WIN
        if (
            self.match.team1_score > self.match.team2_score
            and self.team1_score > self.team2_score
        ):
            score = score + 1
        # TEAM2 WIN
        if (
            self.match.team1_score < self.match.team2_score
            and self.team1_score < self.team2_score
        ):
            score = score + 1

        return score
