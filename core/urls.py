from dj_rest_auth.registration.views import (
    ConfirmEmailView,
    ResendEmailVerificationView,
    VerifyEmailView,
)
from dj_rest_auth.views import PasswordResetConfirmView
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

from core import views

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Prode API",
        default_version="1.0.0",
        description="API documentation of App",
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Swagger documentation
    path(
        "api/v1/",
        include(
            [
                path("prode/", include(("prode.urls", "prode"), namespace="prode")),
                path("user/", include(("user.urls", "user"), namespace="user")),
                path(
                    "swagger/schema/",
                    schema_view.with_ui("swagger", cache_timeout=0),
                    name="swagger-schema",
                ),
            ]
        ),
    ),
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
