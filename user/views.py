from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics, authentication, permissions
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from user.models import Player
from user.serializers import PlayerSerializer


class PlayersList(generics.ListAPIView):
    """
    List view of player model
    """

    permission_classes = [IsAuthenticated]
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail, update and delete view for Player model
    """

    permission_classes = [IsAuthenticated]
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer



