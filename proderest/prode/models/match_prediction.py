from django.db import models

from prode.models.match import MatchResult


class MatchPrediction(models.Model):
    
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    match = models.ForeignKey('prode.Match', on_delete=models.CASCADE)
    prediction = models.TextField(
        choices=MatchResult.choices,
    )
    match_prediction = models.BooleanField(default=False)
    
    def __str__(self):
        return f'({self.id}) {self.match.name}'