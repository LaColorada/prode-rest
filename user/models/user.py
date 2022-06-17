from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone


# User = get_user_model()


class UserManager(BaseUserManager):
    """User management"""

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves new user
        """

        if not email:
            raise ValueError("Users must have an email ")
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create superuser
        """

        user = self._create_user(email, password, True, True, **extra_fields)

        # Creates a new superuser with verified email
        UserManager.create_email_address_entry(user, True, True)
        user.save(using=self._db)

        return user

    @classmethod
    def create_email_address_entry(cls, user, verified, primary):
        # Add verified email address to superuser creation
        try:
            from allauth.account.models import EmailAddress

            EmailAddress.objects.create(
                user=user, email=user.email, verified=verified, primary=primary
            )
        except:
            print(
                "Superuser has not been added to EmailAddress all-auth table. Add it manually please!"
            )


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom model for email login instead of user login
    """

    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
