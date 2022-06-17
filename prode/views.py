from rest_framework import generics

from prode.models import Match, Forecast, Team
from prode.serializers import MatchSerializer, ForecastSerializer, TeamSerializer

from user.models import User
from user.serializers import UserSerializer


class ScoreRankList(generics.ListAPIView):
    """
    List of user depending score
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_queryset(self):
    #     scores = []
    #     for user in User.objects.all():
    #         scores.append(
    #             {
    #                 "user": user,
    #                 "score": sum(
    #                     [
    #                         forecast.score()
    #                         for forecast in Forecast.objects.filter(user=user)
    #                     ]
    #                 ),
    #             }
    #         )
    # for row in enumerate(sorted(scores, key=lambda xxx: xxx["score"], reverse=True), 1):
    #     row[1]["position"] = row[0]
    # return User.objects.all()

    def score_rank(self):
        pass


class MatchCreate(generics.CreateAPIView):

    serializer_class = MatchSerializer

    def get_queryset(self):
        return Match.objects.all()

    def perform_create(self, serializer):

        pk = self.kwargs.get("pk")
        match = Match.objects.get(pk=pk)

        forecast_queryset = Forecast.objects.filter(match=match)
        for forecast in forecast_queryset:
            forecast.player.score = Forecast.score()
            forecast.save()

        serializer.save(match=match)


class MatchList(generics.ListCreateAPIView):
    """
    List View for Match
    """

    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    # def get_queryset(self):
    #     pk = self.kwargs['pk']
    #     return Match.objects.filter(property=pk)


class MatchDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    CRUD view for Match
    """

    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class ForecastList(generics.ListCreateAPIView):
    """
    List View for Forecast
    """

    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer


class TeamList(generics.ListCreateAPIView):
    """
    List View for Team
    """

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
