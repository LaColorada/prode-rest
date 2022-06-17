from django.contrib import admin
from django.urls import include, path

from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # The whole application home is loaded once all views are loaded
    path("", views.app_home, name="app-home"),
    # Prode application
    path("prode/", include("prode.urls")),
    # AllAuth
    path("accounts/", include("allauth.urls")),
    # Rest Auth
    path("auth/", include("dj_rest_auth.urls")),
]
