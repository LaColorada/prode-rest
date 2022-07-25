from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from prode.models import Forecast, Match, Team, Tournament
from prode.serializers import ForecastSerializer
from rest_framework import status
from rest_framework.test import APIClient
from user.models import Player

FORECAST_URL = reverse("forecast-list")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def sample_player(user, score=10):
    """
    Create and return Player
    """

    return Player.objects.create(user=user, score=score)


def sample_tournament(name="Champions League", location="Europe"):
    """
    Create and return Tournament object
    """

    return Tournament.objects.create(name=name, location=location)


def sample_team1(name="Real Madrid", location="Spain"):
    """
    Create and return Team1
    """

    return Team.objects.create(name=name, location=location)


def sample_team2(name="Liverpool", location="England"):
    """
    Create and return Team2
    """

    return Team.objects.create(name=name, location=location)


def forecast_detail_url(match_id):
    """
    Returns forecast detail url
    """
    return reverse("forecast-detail", args=[match_id])


def sample_match(**params):
    """
    Create and return Match object
    """
    defaults = {
        "name": "Real Madrid vs Liverpool",
        "tournament": sample_tournament(),
        "start_date": timezone.now(),
        "duration_mins": 90,
        "match_end": False,
        "team1": sample_team1(),
        "team2": sample_team2(),
        "team1_score": 3,
        "team2_score": 1,
    }
    defaults.update(params)

    return Match.objects.create(**defaults)


def sample_forecast(user, **params):
    """
    Create and return recipe
    """
    defaults = {
        "player": sample_player(user),
        "match": sample_match(),
        "team1_score": 3,
        "team2_score": 1,
    }
    defaults.update(params)

    return Forecast.objects.create(**defaults)


class PublicForecastApiTests(TestCase):
    """
    Test Forecast public API
    """

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """
        Test required authentication
        """
        res = self.client.get(FORECAST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateForecastApiTests(TestCase):
    """
    Test Forecast private API
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@testarudo.com",
            "pass123456",
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_forecast(self):
        """
        Test forecast retrieve
        """
        sample_forecast(user=self.user)

        res = self.client.get(FORECAST_URL)

        forecast = Forecast.objects.all().order_by("id")
        serializer = ForecastSerializer(forecast, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_forecast_limited_to_player(self):
        """
        Test that retrieved forecast belong to player
        """
        user2 = get_user_model().objects.create_user(
            "test@test2.com",
            "pass123456",
        )

        team1 = sample_team1(name="Inter")
        team2 = sample_team2(name="Milan")

        match = sample_match(
            name="Inter vs Milan",
            team1=team1,
            team2=team2,
        )

        player = Player.objects.create(user=user2, score=2)
        player2 = Player.objects.create(user=self.user, score=2)

        Forecast.objects.create(
            player=player, match=match, team1_score=3, team2_score=1
        )
        Forecast.objects.create(
            player=player2, match=match, team1_score=3, team2_score=1
        )

        res = self.client.get(FORECAST_URL)

        player_id = player.id
        forecast = Forecast.objects.filter(player=player_id)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(forecast.count(), 1)

    def test_view_forecast_detail(self):
        """
        Test view Forecast details
        """
        user3 = get_user_model().objects.create_user(
            "test@test3.com",
            "pass123456",
        )

        forecast = sample_forecast(user=user3)

        url = forecast_detail_url(forecast.id)
        res = self.client.get(url)

        serializer = ForecastSerializer(forecast)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_forecast(self):
        """
        Test create new Forecast
        """

        match = sample_match(
            name="Benfica vs Sevilla",
            tournament=sample_tournament(name="Europa League"),
            start_date=timezone.now(),
            duration_mins=90,
            match_end=False,
            team1=sample_team1(name="Benfica", location="Portugal"),
            team2=sample_team2(name="Sevilla", location="Spain"),
            team1_score=2,
            team2_score=2,
        )
        # print(self.user)
        # print(match)
        sample_player(user=self.user, score=1)
        payload = {
            "player": 1,
            "match": 1,
            "team1_score": 3,
            "team2_score": 1,
        }

        res = self.client.post(FORECAST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        forecast = Forecast.objects.get(id=res.data["id"])
        self.assertEqual(str(payload["player"]), str(forecast.player)[1])
