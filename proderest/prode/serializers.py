from rest_framework import serializers

from django.contrib.auth import get_user_model

from prode.models import Match, MatchPrediction, Team



class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for object user 
    """
    
    class Meta:
        model = Team
        fields = ('__all__')


class MatchSerializer(serializers.ModelSerializer):
    """
    Serializer for object user 
    """
    team1 = TeamSerializer()
    team2 = TeamSerializer()
    
    class Meta:
        model = Match
        fields = ('__all__')
      
      
class MatchPredictionSerializer(serializers.ModelSerializer):
    """
    Serializer for object user 
    """
    
    class Meta:
        model = MatchPrediction
        fields = ('__all__')

