from dj_rest_auth.registration.views import (
    ConfirmEmailView,
    ResendEmailVerificationView,
    VerifyEmailView,
)
from dj_rest_auth.views import PasswordResetConfirmView
from django.contrib import admin
from django.urls import include, path

from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # The whole application home is loaded once all views are loaded
    path("", views.ApiHome.as_view(), name="api-home"),
    # Prode application
    path("prode/", include("prode.urls")),
    # User application
    path("user/", include("user.urls")),
    # account confirm email must be first before any other dj_rest_auth view
    path(
        "auth/account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    # AllAuth
    path("accounts/", include("allauth.urls")),
    # Rest Auth
    path(
        "auth/registration/account-confirm-email/<str:key>/", ConfirmEmailView.as_view()
    ),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "auth/registration/resend-email",
        ResendEmailVerificationView.as_view(),
        name="resend-email",
    ),
    path(
        "auth/password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
