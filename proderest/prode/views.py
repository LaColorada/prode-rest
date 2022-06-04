from rest_framework import generics

from prode.models import Match, MatchPrediction, Team
from prode.serializers import MatchSerializer, MatchPredictionSerializer, TeamSerializer


class MatchList(generics.ListAPIView):
    """ 
    Creates new user in system
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class MatchPredictionList(generics.ListAPIView):
    """ 
    Creates new user in system
    """
    queryset = MatchPrediction.objects.all()
    serializer_class = MatchPredictionSerializer
    

class TeamList(generics.ListAPIView):
    """ 
    Creates new user in system
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
