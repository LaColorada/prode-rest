from rest_framework import serializers

from prode.models import Match, Forecast, Team, Tournament

from user.serializers import PlayerSerializer


class TournamentSerializer(serializers.ModelSerializer):
    """
    Serializer for Tournament model
    """

    class Meta:
        model = Tournament
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for Team model
    """

    tournament = TournamentSerializer(many=True, read_only=True)

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

    player = PlayerSerializer()

    class Meta:
        model = Forecast
        fields = "__all__"
