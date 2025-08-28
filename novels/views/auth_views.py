from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import generics, status
from novels.models import User
from novels.serializers import UserCreateSerializer


class UserLoginView(APIView):
    """
    we used APIVIEW here as it provide the default get
    and post methods. Since when we log in , we need to 
    get the user entered login from the post request,
    we can extract the username and password from the
    request and authenticate it using authenticate function.
    if user is there, then we give the refresh token in a 
    response which we can use as a token to store in the 
    cache.

    """
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username = username, password = password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        
        return Response({'error': 'Invalid credentials'}, status = status.HTTP_401_UNAUTHORIZED)

class UserCreateView(generics.CreateAPIView):
    """
    We needed a separate router for the user creation apart from the 
    ViewSets which give a single url, so we created the user with the
    CreateAPIView instead of the viewsets.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = UserCreateSerializer

