from rest_framework.routers import DefaultRouter
from .views import UserViewSet, NovelViewSet, UserCreateView, UserLoginView, NovelCommentViewSet, PaymentCreationView
from novels.views.chapter_views import ChapterViewSet
from django.urls import path
from rest_framework_nested.routers import NestedDefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('register', UserCreateView.as_view()),
    path('login', UserLoginView.as_view()),
    # path('novels/<int:pk>/purchase', UserCreateView.as_view())
]


router.register('user', UserViewSet)
router.register('novels', NovelViewSet, basename='novel')
novels_router = NestedDefaultRouter(router, 'novels', lookup= 'novel')
novels_router.register('comments',NovelCommentViewSet, basename='novel-comments')
novels_router.register('chapters', ChapterViewSet, basename='novel-chapters')
novels_router.register('purchase', PaymentCreationView, basename='novel-payments')

urlpatterns+= router.urls
urlpatterns+= novels_router.urls
