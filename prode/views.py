from rest_framework import generics

from prode.models import Match, Forecast, Team, Tournament
from prode.serializers import (
    MatchSerializer,
    ForecastSerializer,
    TeamSerializer,
    TournamentSerializer,
)

from user.models import User
from user.serializers import UserSerializer



class MatchList(generics.ListCreateAPIView):
    """
    List View for Match model
    """

    serializer_class = MatchSerializer

    def get_queryset(self):
        return Match.objects.all()


class MatchDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail, update and delete view for Match model
    """

    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class ForecastList(generics.ListCreateAPIView):
    """
    List View for Forecast model
    """

    serializer_class = ForecastSerializer

    def get_queryset(self):
        return Forecast.objects.all()


class ForecastDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail, update and delete view for Forecast model
    """

    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer


class TeamList(generics.ListCreateAPIView):
    """
    List View for Team model
    """

    serializer_class = TeamSerializer

    def get_queryset(self):
        return Team.objects.all()


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail, update and delete view for Team model
    """

    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TournamentList(generics.ListCreateAPIView):
    """
    List View for Tournament model
    """

    serializer_class = TournamentSerializer

    def get_queryset(self):
        return Tournament.objects.all()


class TournamentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail, update and delete view for Tournament model
    """

    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
