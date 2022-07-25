from core.permissions import IsAdminOrReadOnly
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from user.models import Player

from prode.models import Forecast, Match, Team, Tournament
from prode.serializers import (
    ForecastSerializer,
    MatchSerializer,
    TeamSerializer,
    TournamentSerializer,
)


class MatchList(generics.ListAPIView):
    """
    List View for Match model
    """

    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Match.objects.all()


class MatchDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail, update and delete view for Match model
    """

    permission_classes = [IsAdminOrReadOnly]
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class ForecastList(generics.ListCreateAPIView):
    """
    List View for Forecast model
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ForecastSerializer

    def get_queryset(self):
        return Forecast.objects.all()

    def perform_create(self, serializer):
        player = Player.objects.get(user=self.request.user)
        serializer.save(player=player)


class ForecastDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail, update and delete view for Forecast model
    """

    permission_classes = [IsAuthenticated]
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer


class TeamList(generics.ListAPIView):
    """
    List View for Team model
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer

    def get_queryset(self):
        return Team.objects.all()


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail, update and delete view for Team model
    """

    permission_classes = [IsAdminOrReadOnly]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TournamentList(generics.ListAPIView):
    """
    List View for Tournament model
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TournamentSerializer

    def get_queryset(self):
        return Tournament.objects.all()


class TournamentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail, update and delete view for Tournament model
    """

    permission_classes = [IsAdminOrReadOnly]
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
