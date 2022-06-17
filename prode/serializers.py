from rest_framework import serializers

from django.contrib.auth import get_user_model

from prode.models import Match, Forecast, Team, Player


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for Team model
    """

    class Meta:
        model = Team
        fields = "__all__"


class MatchSerializer(serializers.ModelSerializer):
    """
    Serializer for Match model
    """

    team1 = TeamSerializer()
    team2 = TeamSerializer()

    class Meta:
        model = Match
        fields = "__all__"


class ForecastSerializer(serializers.ModelSerializer):
    """
    Serializer for Forecast model
    """

    class Meta:
        model = Forecast
        fields = "__all__"


class PlayerSerializer(serializers.ModelSerializer):
    """
    Serializer for Forecast model
    """

    class Meta:
        model = Player
        fields = "__all__"
