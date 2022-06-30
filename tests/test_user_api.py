from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("rest_register")
TOKEN_URL = reverse("rest_login")
ME_URL = reverse("rest_user_details")
VERIFY_EMAIL_URL = reverse("rest_verify_email")
RESEND_EMAIL_URL = reverse("rest_resend_email")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
    Test public user API
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        Test user creation with a successful payload
        """

        payload = {
            "email": "test@test.com",
            "password1": "pass123456",
            "password2": "pass123456",
            "first_name": "Firstname",
            "last_name": "Lastname",
        }

        # response
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password1"]))
        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        """
        Test already created user exists
        """

        payload = {
            "email": "test@test.com",
            "password": "pass123456",
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Password must be longer than 5 chars
        """

        payload = {"email": "test@test.com", "password": "pw"}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """
        Prove that the token in created by user
        """

        payload = {
            "email": "test@test.com",
            "password": "pass123456",
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("access_token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """
        Prove that the token is not created with invalid credentials
        """

        create_user(email="test@test.com", password="pass123456")
        payload = {
            "email": "test@test.com",
            "password": "wrong",
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """
        Prove that the token is not created if theres no user
        """

        payload = {
            "email": "test@test.com",
            "password": "pass123456",
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """
        Test that email and password are requiered
        """

        res = self.client.post(TOKEN_URL, {"email": "one", "password": ""})

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """
        Proves that user authentication is required for users
        """

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """
    Test private user API
    """

    def setUp(self):
        self.user = create_user(
            email="test@test.com",
            password="pass123456",
            first_name="Firstname",
            last_name="Lastname",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """
        Test retrieve profile for user with login
        """

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            {
                "email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
            },
        )

    def test_post_me_not_allowed(self):
        """
        Test that POST is not allowed
        """

        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """
        Prove that user is being updated if he is authenticated
        """

        payload = {
            "first_name": "New firstname",
            "last_name": "New lastname",
            "password": "pass123456",
        }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload["first_name"])
        self.assertEqual(self.user.last_name, payload["last_name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
