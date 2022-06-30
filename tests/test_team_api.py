from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from prode.models import Team
from prode.serializers import TeamSerializer
from rest_framework import status
from rest_framework.test import APIClient

TEAM_URL = reverse("team-list")


class PublicTeamApiTests(TestCase):
    """
    Test team public API
    """

    def setUp(self):
        self.client = APIClient()

    def test_login_requiered(self):
        """
        Tests that login is requiered to obtain team
        """

        res = self.client.get(TEAM_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTeamApiTests(TestCase):
    """
    Test team private API
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@testarudo.com",
            "pass123456",
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_team(self):
        """
        Test tag retrieve
        """
        Team.objects.create(name="Real Madrid", location="Spain")
        Team.objects.create(name="Liverpool", location="England")

        res = self.client.get(TEAM_URL)

        team = Team.objects.all().order_by("-name")
        serializer = TeamSerializer(team, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
