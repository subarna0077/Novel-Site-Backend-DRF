from rest_framework.routers import DefaultRouter
from .views import UserViewSet, NovelViewSet, UserCreateView, UserLoginView
from django.urls import path


router = DefaultRouter()

urlpatterns = [
    path('register', UserCreateView.as_view()),
    path('login', UserLoginView.as_view()),
]


router.register('user', UserViewSet)
router.register('novel', NovelViewSet)

urlpatterns += router.urls