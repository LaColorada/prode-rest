from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from prode.models import Forecast, Match, Team, Tournament
from user.models import Player


def sample_user(email="test@test.com", password="pass123456"):
    """
    Creates sample user for testing
    """

    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    """
    Test model creation
    """

    def test_create_user_with_email_successful(self):
        """
        Test to create user with email successfully
        """

        email = "test@mail.com"
        password = "pass123456"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Email test for custom user
        """

        email = "test@TEST.COM"
        user = get_user_model().objects.create_user(email, "pass123456")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        New user invalid email
        """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "pass123456")

    def test_create_new_superuser(self):
        """
        Test created superuser
        """

        email = "test@mail.com"
        password = "pass123456"
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_player_str(self):
        """
        Test player as text string
        """
        player = Player.objects.create(
            user=sample_user(),
            score="10",
        )

        self.assertEqual(str(player), f"({player.id}) ({player.user.email})")

    def test_team_str(self):
        """
        Test team as text string
        """
        team = Team.objects.create(
            name="Real Madrid",
            location="Spain",
        )

        self.assertEqual(str(team), f"({team.id}) ({team.name})")

    def test_tournament_str(self):
        """
        Test tournament as text string
        """
        tournament = Tournament.objects.create(
            name="Champions League",
            location="Europe",
        )

        self.assertEqual(str(tournament), f"({tournament.id}) ({tournament.name})")

    def test_match_str(self):
        """
        Test match as text string
        """
        match = Match.objects.create(
            name="Real Madrid vs Liverpool",
            tournament=Tournament.objects.create(
                name="Champions League", location="Europe"
            ),
            start_date=timezone.now(),
            duration_mins=90,
            team1=Team.objects.create(name="Real Madrid", location="Spain"),
            team2=Team.objects.create(name="Liverpool", location="England"),
            team1_score=3,
            team2_score=1,
        )

        self.assertEqual(str(match), f"({match.id}) ({match.name})")

    def test_forecast_str(self):
        """
        Test forecast as text string
        """
        forecast = Forecast.objects.create(
            player=Player.objects.create(
                user=sample_user(),
                score="10",
            ),
            match=Match.objects.create(
                name="Real Madrid vs Liverpool",
                tournament=Tournament.objects.create(
                    name="Champions League", location="Europe"
                ),
                start_date=timezone.now(),
                duration_mins=90,
                team1=Team.objects.create(name="Real Madrid", location="Spain"),
                team2=Team.objects.create(name="Liverpool", location="England"),
                team1_score=3,
                team2_score=1,
            ),
            team1_score=3,
            team2_score=1,
        )

        self.assertEqual(
            str(forecast), f"({forecast.id}) {forecast.match.name} | {forecast.player}"
        )
