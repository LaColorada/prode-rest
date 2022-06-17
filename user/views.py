from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics, authentication, permissions
from rest_framework.settings import api_settings

from user import serializers



class CreateUserView(generics.CreateAPIView):
    """ 
    Creates new user in system
    """

    serializer_class = serializers.UserSerializer


class CreateTokenView(ObtainAuthToken):
    """ 
    Create new auth token for user 
    """
    
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    

class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Manages authenticated user
    """
    
    serializer_class = serializers.UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        """
        Retrieve and return authenticated user
        """
        
        return self.request.user