from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from novels.models import Novel, Comment
from novels.serializers import CommentSerializer
from novels.permissions import IsCommentOwnerOrAuthorOrReadOnly

class NovelCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCommentOwnerOrAuthorOrReadOnly]

    def get_queryset(self):
        novel_slug = self.kwargs.get('novel_pk')  # Fixed the bug from your original code
        if novel_slug:
            return Comment.objects.filter(novel__slug=novel_slug)
        return super().get_queryset()