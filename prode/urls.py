from django.urls import path

from prode import views

urlpatterns = [
    path("matches/", views.MatchList.as_view(), name="match-list"),
    path("matches/create/", views.MatchCreate.as_view(), name="match-create"),
    path("matches/<int:pk>/", views.MatchDetail.as_view(), name="match-detail"),
    path("forecasts/", views.ForecastList.as_view(), name="forecast-list"),
    path("teams/", views.TeamList.as_view(), name="team-list"),
    path("score-rank/", views.ScoreRankList.as_view(), name="scorerank-list"),
]
