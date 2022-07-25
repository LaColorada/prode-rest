from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from prode.models import Tournament
from prode.serializers import TournamentSerializer
from rest_framework import status
from rest_framework.test import APIClient

TOURNAMENT_URL = reverse("tournament-list")


class PublicTournamentApiTests(TestCase):
    """
    Test Tournament public API
    """

    def setUp(self):
        self.client = APIClient()

    def test_login_requiered(self):
        """
        Tests that login is requiered to obtain tournament
        """

        res = self.client.get(TOURNAMENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTournamentApiTests(TestCase):
    """
    Test Tournament private API
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@testarudo.com",
            "pass123456",
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tournament(self):
        """
        Test tag retrieve
        """
        Tournament.objects.create(name="Real Madrid", location="Spain")
        Tournament.objects.create(name="Liverpool", location="England")

        res = self.client.get(TOURNAMENT_URL)

        tournament = Tournament.objects.all().order_by("-name")
        serializer = TournamentSerializer(tournament, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
