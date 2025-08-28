from rest_framework.routers import DefaultRouter
from .views import UserViewSet, NovelViewSet, UserCreateView, UserLoginView, NovelCommentViewSet
from django.urls import path
from rest_framework_nested.routers import NestedDefaultRouter


router = DefaultRouter()

urlpatterns = [
    path('register', UserCreateView.as_view()),
    path('login', UserLoginView.as_view()),
]


router.register('user', UserViewSet)
router.register('novels', NovelViewSet, basename='novel')
novels_router = NestedDefaultRouter(router, 'novels', lookup= 'novel')
novels_router.register('comments',NovelCommentViewSet, basename='novel-comments')

urlpatterns+= router.urls
urlpatterns+= novels_router.urls
