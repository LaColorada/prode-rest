from django.db import transaction
from rest_framework import serializers

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, PasswordResetConfirmSerializer

from user.models import Player


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for object user
    """

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "first_name", "last_name")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
            }
        }

    def create(self, **validated_data):
        """
        Create new user with encrypted password and return it
        """

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Updates user and return correct configurated password
        """

        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

            return user


class PlayerSerializer(serializers.ModelSerializer):
    """
    Serializer for Forecast model
    """

    user = UserSerializer()

    class Meta:
        model = Player
        fields = "__all__"


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for the user authentication object
    """

    email = serializers.CharField()
    password = serializers.CharField(
        trim_whitespace=False,
        style={"input_type": "password"},
    )

    def validate(self, attrs):
        """
        Validate and authenticate user
        """

        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


################ CUSTOM REST AUTH SERIALIZERS #############################
class RegistrationSerializer(RegisterSerializer):
    username = None
    password1 = serializers.CharField(style={"input_type": "password"})
    password2 = serializers.CharField(style={"input_type": "password"})

    @transaction.atomic
    def save(self, request):
        """Define transaction.atomic to rollback in case of error"""
        user = super().save(request)
        user.save()
        return user


class LoginSerializer(LoginSerializer):
    username = None


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email"]


class PasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    new_password1 = serializers.CharField(style={"input_type": "password"})
    new_password2 = serializers.CharField(style={"input_type": "password"})
