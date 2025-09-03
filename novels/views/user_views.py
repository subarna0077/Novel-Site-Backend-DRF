from rest_framework import viewsets, status
from novels.models import User, Comment, PurchasedNovel
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from novels.serializers import UserCreateSerializer , UserPreviewSerializer, CommentSerializer, PurchasedNovelSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from novels.permissions import IsSelfOrAdmin


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
    @action(detail=False, methods=["get"], url_path="me", permission_classes=[IsAuthenticated])
    def me(self, request):
    # Uses whatever serializer get_serializer_class() returns for action='get'
    # Passing request.user as instance for serialization (object → JSON)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='me/comments', permission_classes = [IsAuthenticated])
    def list_comments(self,request):
        user = request.user
        user_comments = user.user_comments.all()
        serializer = CommentSerializer(user_comments, many=True)
        return Response(serializer.data)

    @action(detail = False, methods=['patch', 'delete','get'], url_path='me/comments/(?P<comment_id>\d+)', permission_classes = [IsAuthenticated])
    def comments(self,request, comment_id = None):
        user = request.user
        try:
            comment = user.user_comments.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response({"error": "Comment does not exists."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        
        if request.method == 'PATCH':
            serializer = CommentSerializer(comment, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        
        if request.method == 'DELETE':
            comment.delete()
            return Response({"message": "Comment deleted successfully"},status = status.HTTP_204_NO_CONTENT)
        
    @action(detail = False, methods=['get'], url_path='me/purchased-novels', permission_classes=[IsAuthenticated])
    def get_purchased_novels(self, request):
        user = request.user
        novels = PurchasedNovel.objects.filter(user = user)
        serializer = PurchasedNovelSerializer(novels, many=True)
        return Response(serializer.data)

