from django.contrib import admin
from django.urls import include, path

from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView
from dj_rest_auth.views import PasswordResetConfirmView

from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # The whole application home is loaded once all views are loaded
    path("", views.ApiHome.as_view(), name="api-home"),
    # Prode application
    path("prode/", include("prode.urls")),
    # User application
    path("user/", include("user.urls")),
    # AllAuth
    path("accounts/", include("allauth.urls")),
    # Rest Auth
    # account confirm email must be first before any other dj_rest_auth view
    path(
        "auth/registration/account-confirm-email/<str:key>/", ConfirmEmailView.as_view()
    ),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "auth/account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    path(
        "auth/password/reset/confirm/<slug:uidb64>/<slug:token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
