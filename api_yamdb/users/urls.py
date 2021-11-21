from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CodeConfirmView, SignupView, UserModelViewset

router = DefaultRouter()
router.register('users', UserModelViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', SignupView.as_view()),
    path('auth/token/', CodeConfirmView.as_view()),
]
