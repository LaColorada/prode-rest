from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from rest_framework.decorators import api_view
from django.urls import path, include


class ApiHome(APIView):
    """
    This is the main application endpoint.
    From this endpoint you can explore each resources by clicking in each link below.
    """

    # permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        response = {
            "prode": {
                "player-list": reverse("player-list", request=request),
                "forecast-list": reverse("forecast-list", request=request),
                "tournament-list": reverse("tournament-list", request=request),
                "team-list": reverse("team-list", request=request),
                "match-list": reverse("match-list", request=request),
            },
            "user": {
                # Authentication endpoints
                "login": reverse("rest_login", request=request),
                "user": reverse("rest_user_details", request=request),
                "logout": reverse("rest_logout", request=request),
                "password_reset": reverse("rest_password_reset", request=request),
                "password_change": reverse("rest_password_change", request=request),
                # Register endpoints
                "register": reverse("rest_register", request=request),
                "verify_email": reverse("rest_verify_email", request=request),
                "resend_email": reverse("rest_resend_email", request=request),
                # Token endpoints
                "token_verify": reverse("token_verify", request=request),
                "token_refresh": reverse("token_refresh", request=request),
            },
        }
        return Response(response, status=status.HTTP_200_OK)


#     def post(self, request):
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
