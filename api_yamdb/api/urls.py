from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (APIUser, UserViewSet, get_jwt_token,
                    send_confirmation_code, ReviewViewSet,
                    CommentViewSet, TitletViewSet)


router = DefaultRouter()
router.register('users', UserViewSet)
router.register(r'titles', TitletViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')


urlpatterns = [
    path('v1/auth/email/', send_confirmation_code, name='get_token'),
    path('v1/auth/token/', get_jwt_token, name='send_confirmation_code'),
    path('v1/users/me/', APIUser.as_view()),
    path('v1/', include(router.urls)),
]
