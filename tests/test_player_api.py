from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user.models import Player
from user.serializers import PlayerSerializer

PLAYER_URL = reverse("player-list")


class PublicPlayerApiTests(TestCase):
    """
    Test Player public API
    """

    def setUp(self):
        self.client = APIClient()

    def test_login_requiered(self):
        """
        Tests that login is requiered to obtain Player
        """

        res = self.client.get(PLAYER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePlayerApiTests(TestCase):
    """
    Test Player private API
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@testarudo.com",
            "pass123456",
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_player(self):
        """
        Test Player retrieve
        """
        Player.objects.create(user=self.user, score=8)

        res = self.client.get(PLAYER_URL)

        player = Player.objects.all().order_by("-score")
        serializer = PlayerSerializer(player, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
