from django.urls import path

from prode import views

urlpatterns = [
    path('matches/', views.MatchList.as_view(), name='match-list'),
    path('match-predictions/', views.MatchPredictionList.as_view(), name='matchprediction-list'),
    path('teams/', views.TeamList.as_view(), name='team-list'),
]
