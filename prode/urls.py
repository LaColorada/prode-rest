from django.urls import path

from prode import views

urlpatterns = [
    # Player URLs
    # Match URLs
    path("matches/", views.MatchList.as_view(), name="match-list"),
    path("matches/<int:pk>/", views.MatchDetail.as_view(), name="match-detail"),
    # Forecast URLs
    path("forecasts/", views.ForecastList.as_view(), name="forecast-list"),
    path("forecasts/<int:pk>/", views.ForecastDetail.as_view(), name="forecast-detail"),
    # Team URLs
    path("teams/", views.TeamList.as_view(), name="team-list"),
    path("teams/<int:pk>/", views.TeamDetail.as_view(), name="team-detail"),
    # Tournaments URLs
    path("tournaments/", views.TournamentList.as_view(), name="tournament-list"),
    path(
        "tournaments/<int:pk>/",
        views.TournamentDetail.as_view(),
        name="tournament-detail",
    ),
]
