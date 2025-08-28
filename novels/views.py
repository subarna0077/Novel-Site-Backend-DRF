from .views.novel_views import NovelViewSet
from .views.auth_views import UserCreateView, UserLoginView
from .views.comment_views import NovelCommentViewSet
from .views.user_views import UserViewSet


# from django.shortcuts import get_object_or_404
# from rest_framework import viewsets, generics
# from .models import User, Novel, Comment
# from .serializers import UserCreateSerializer, UserPreviewSerializer, NovelSerializer, CommentSerializer
# from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission, IsAdminUser, SAFE_METHODS
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.views import APIView
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.decorators import action

# # Create your views here.

# class IsSelfOrAdmin(BasePermission):
#     def has_object_permission(self, request, view, obj):

#         ## we returned boolean here because this class check if it pass the permission or not. if we returned true, permission is given otherwise denied
#         return request.user.is_staff or obj == request.user

# class IsNovelOwnerOrAdmin(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.is_staff or obj.author == request.user
    
# class IsCommentOwnerOrAuthorOrReadOnly(BasePermission):   

#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True
        
#         user = request.user

#         if not request.user or not request.user.is_authenticated:
#             return False
        
#         return (
#             obj.user_id == user.id or
#             obj.novel.author_id == user.id or
#             user.is_staff
#         )

# class UserLoginView(APIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         user = authenticate(username = username, password = password)

#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token)
#             })
        
#         return Response({'error': 'Invalid credentials'}, status = status.HTTP_401_UNAUTHORIZED)

# class UserCreateView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = [AllowAny]
#     authentication_classes = []
#     serializer_class = UserCreateSerializer


# class UserViewSet(viewsets.ModelViewSet): ## create update delete list users
#     queryset = User.objects.all()
#      ## anyone can get request but for the post update patch, authentication is required
#     authentication_classes = [JWTAuthentication]

#     def get_permissions(self):
#         if self.action == 'create':
#             return [AllowAny()]
        
#         if self.action in ["list", "destroy"]:
#             return [IsAdminUser()]
        
#         if self.action in ["retrieve", "update", "partial_update"]:
#             return [IsAuthenticated(), IsSelfOrAdmin()]
        
#         ##default fallback
#         return [IsAuthenticated()]

#     def get_serializer_class(self):
#         if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
#             return UserCreateSerializer
#         return UserPreviewSerializer
    
#     ## Custom action for /me

#     """
#     detail = True -> the action is tied to a single object
#     detail = False -> the action is tied to the entire collection i.e. does'nt need a id
#     """
#     @action(detail=False, methods=["get"], url_path="me", permission_classes=[IsAuthenticated])
#     def me(self, request):
#     # Uses whatever serializer get_serializer_class() returns for action='get'
#     # Passing request.user as instance for serialization (object → JSON)
#         serializer = self.get_serializer(request.user)
#         return Response(serializer.data)
    
#     @action(detail=False, methods=['get'], url_path='me/comments', permission_classes = [IsAuthenticated])
#     def list_comments(self,request):
#         user = request.user
#         user_comments = user.user_comments.all()
#         serializer = CommentSerializer(user_comments, many=True)
#         return Response(serializer.data)

#     @action(detail = False, methods=['patch', 'delete','get'], url_path='me/comments/(?P<comment_id>\d+)', permission_classes = [IsAuthenticated])
#     def comments(self,request, comment_id = None):
#         user = request.user
#         try:
#             comment = user.user_comments.get(pk=comment_id)
#         except Comment.DoesNotExist:
#             return Response({"error": "Comment does not exists."}, status=status.HTTP_404_NOT_FOUND)
        
#         if request.method == 'GET':
#             serializer = CommentSerializer(comment)
#             return Response(serializer.data)
        
#         if request.method == 'PATCH':
#             serializer = CommentSerializer(comment, data=request.data, partial = True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        
#         if request.method == 'DELETE':
#             comment.delete()
#             return Response({"message": "Comment deleted successfully"},status = status.HTTP_204_NO_CONTENT)



# class NovelViewSet(viewsets.ModelViewSet): ## create, update, delete, list novels
#     queryset = Novel.objects.all()
#     serializer_class = NovelSerializer
#     authentication_classes = [JWTAuthentication]
#     lookup_field = "slug"

#     def get_permissions(self):
#         if self.action == 'list':
#             return [AllowAny()]
        
#         if self.action in ['create', 'retrieve']:
#             return [IsAuthenticated()]
            
#         if self.action in ['update', 'partial_update', 'destroy']:
#             return [IsAuthenticated(), IsNovelOwnerOrAdmin()]
        
#         return [IsAuthenticated()]

#     def perform_create(self, serializer):
#         serializer.save(author = self.request.user)

#     @action(detail = False, methods=['get'], url_path="my-novels")
#     def my_novels(self, request):
#         novels = Novel.objects.filter(author = request.user)

#         ## this get_serializer gets the whatever serializer the get method is using and we passed the novels inside by filtering according to the logged in users.
#         serializer = self.get_serializer(novels, many=True)
#         return Response(serializer.data)
    
# class NovelCommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsCommentOwnerOrAuthorOrReadOnly]

#     def get_queryset(self):
#         novel_slug = self.kwargs(['novel_pk'])
#         if novel_slug:
#             return Comment.objects.filter(novel__slug = novel_slug)
#         return super().get_queryset()
