from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from prode.models import Match, Team, Tournament
from prode.serializers import MatchSerializer
from rest_framework import status
from rest_framework.test import APIClient
from user.models import Player

MATCH_URL = reverse("match-list")


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


def match_detail_url(match_id):
    """
    Returns Match detail url
    """
    return reverse("match-detail", args=[match_id])


class PublicMatchApiTests(TestCase):
    """
    Test Match public API
    """

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """
        Test required authentication
        """
        res = self.client.get(MATCH_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMatchApiTests(TestCase):
    """
    Test Match private API
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@testarudo.com",
            "pass123456",
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_match(self):
        """
        Test match retrieve
        """
        sample_match()

        res = self.client.get(MATCH_URL)

        match = Match.objects.all().order_by("id")
        serializer = MatchSerializer(match, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_match_detail(self):
        """
        Test view Match details
        """

        match = sample_match()

        url = match_detail_url(match.id)
        res = self.client.get(url)

        serializer = MatchSerializer(match)
        self.assertEqual(res.data, serializer.data)
