from rest_framework import viewsets
from novels.models import Novel
from novels.serializers import NovelSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from novels.permissions import IsNovelOwnerOrAdmin

class NovelViewSet(viewsets.ModelViewSet): ## create, update, delete, list novels
    queryset = Novel.objects.all()
    serializer_class = NovelSerializer
    authentication_classes = [JWTAuthentication]
    lookup_field = "slug"

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        
        if self.action in ['create', 'retrieve']:
            return [IsAuthenticated()]
            
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsNovelOwnerOrAdmin()]
        
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

    @action(detail = False, methods=['get'], url_path="my-novels")
    def my_novels(self, request):
        novels = Novel.objects.filter(author = request.user)

        ## this get_serializer gets the whatever serializer the get method is using and we passed the novels inside by filtering according to the logged in users.
        serializer = self.get_serializer(novels, many=True)
        return Response(serializer.data)
    