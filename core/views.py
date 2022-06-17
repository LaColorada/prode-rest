from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework.decorators import api_view
from django.urls import path, include


@api_view(["GET"])
# @permission_classes([permissions.IsAuthenticated | permissions.IsAdminUser])
def app_home(request, format=None):
    """
    This is the main application endpoint.
    From this endpoint you can explore each resources by clicking in each link below.
    """
    response = {
        "prode_teams": reverse("team-list", request=request, format=format),
        "prode_matches": reverse("match-list", request=request, format=format),
        "prode_forecast": reverse("forecast-list", request=request, format=format),
        "prode_scorerank": reverse("scorerank-list", request=request, format=format),
        # 'login': reverse('rest_login', request=request, format=format),
        # 'logout': reverse('rest_logout', request=request, format=format),
        # 'password_reset': reverse('rest_password_reset', request=request, format=format),
        # 'register': reverse('rest_register', request=request, format=format),
    }
    return Response(response, status=status.HTTP_200_OK)
