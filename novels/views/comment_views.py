from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from novels.models import Novel, Comment
from novels.serializers import CommentSerializer
from novels.permissions import IsCommentOwnerOrAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated, AllowAny

class NovelCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsCommentOwnerOrAuthorOrReadOnly()]

    def get_queryset(self):
        novel_slug = self.kwargs.get('novel_pk')  # Fixed the bug from your original code
        if novel_slug:
            return Comment.objects.filter(novel__slug=novel_slug)
        return super().get_queryset()