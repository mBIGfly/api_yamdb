from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CodeConfirmView, CommentViewSet,
                    GenreViewSet, ReviewViewSet, SignupView, TitleViewSet,
                    UserModelViewset)

router = DefaultRouter()
router.register('users', UserModelViewset)
router.register(r'titles', TitleViewSet, basename='api_titles')
router.register(r'categories', CategoryViewSet, basename='api_categories')
router.register(r'genres', GenreViewSet, basename='api_genres')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='api_reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='api_comments')


urlpatterns = [
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/auth/token/', CodeConfirmView.as_view(), name='token'),
    path('v1/', include(router.urls)),
]
