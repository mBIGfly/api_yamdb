from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CodeConfirmView, SignupView, UserModelViewset,
                    ReviewViewSet, CommentViewSet, TitleViewSet,
                    CategoryViewSet, GenresViewSet)


router = DefaultRouter()
router.register('users', UserModelViewset)
router.register(r'titles', TitleViewSet, basename='api_titles')
router.register(r'categories', CategoryViewSet, basename='api_categories')
router.register(r'genres', GenresViewSet, basename='api_genres')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='api_reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='api_comments')


urlpatterns = [
    path('v1/auth/signup/', SignupView.as_view()),
    path('v1/auth/token/', CodeConfirmView.as_view()),
    path('v1/', include(router.urls)),
]
