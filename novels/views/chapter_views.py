from novels.models import Chapter, Novel
from novels.serializers import ChapterSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ChapterSerializer

    def get_queryset(self):
        novel_slug = self.kwargs.get('novel_pk')
        if novel_slug:
            return Chapter.objects.filter(novel_id = novel_slug)
        return super().get_queryset()
        





