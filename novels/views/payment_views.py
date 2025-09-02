from novels.serializers import PaymentSerializer
from novels.models import Payment, Novel
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

class PaymentCreationView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    http_method_names = ['post']


    def get_queryset(self):
        novel_id = self.kwargs.get('novel_pk')
        if novel_id:
            return Payment.objects.filter(novel_id = novel_id)

    def perform_create(self, serializer):
        novel_id = self.kwargs.get('novel_pk')
        novel = get_object_or_404(Novel, pk = novel_id)
        serializer.save(user = self.request.user, novel = novel)
 

