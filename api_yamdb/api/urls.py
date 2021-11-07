from django.urls import include, path
from rest_framework import routers

from .views import ReviewViewSet, CommentViewSet, TitletViewSet

router = routers.DefaultRouter()
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
    path('v1/', include(router.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt'))
]
