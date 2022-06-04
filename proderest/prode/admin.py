from django.contrib import admin

from prode.models import Match, MatchPrediction, Team
# Register your models here.

admin.site.register(Match)
admin.site.register(MatchPrediction)
admin.site.register(Team)