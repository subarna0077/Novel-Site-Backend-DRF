from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import User, Novel
from .serializers import UserCreateSerializer, UserPreviewSerializer, NovelSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

# Create your views here.

class IsSelfOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user

class IsNovelOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.author == request.user

class UserLoginView(APIView):
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
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = UserCreateSerializer


class UserViewSet(viewsets.ModelViewSet): ## create update delete list users
    queryset = User.objects.all()
     ## anyone can get request but for the post update patch, authentication is required
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        
        if self.action in ["list", "destroy"]:
            return [IsAdminUser()]
        
        if self.action in ["retrieve", "update", "partial_update"]:
            return [IsAuthenticated(), IsSelfOrAdmin()]
        
        ##default fallback
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return UserCreateSerializer
        return UserPreviewSerializer
    
    ## Custom action for /me

    """
    detail = True -> the action is tied to a single object
    detail = False -> the action is tied to the entire collection i.e. does'nt need a id
    """
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
    # Uses whatever serializer get_serializer_class() returns for action='me'
    # Passing request.user as instance for serialization (object → JSON)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    

class NovelViewSet(viewsets.ModelViewSet): ## create, update, delete, list novels
    queryset = Novel.objects.all()
    serializer_class = NovelSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        
        if self.action in ['create', 'retrieve']:
            return [IsAuthenticated()]
            
        if self.action in ['update', 'partial_update', 'delete']:
            return [IsAuthenticated(), IsNovelOwnerOrAdmin()]
        
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)
