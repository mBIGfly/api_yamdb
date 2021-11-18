from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import (APIUser, SignupView, UserViewSet, get_jwt_token,
                         send_confirmation_code)

router = DefaultRouter()
router.register('users', UserViewSet)


urlpatterns = [
    path('v1/auth/email/', send_confirmation_code, name='get_token'),
    path('v1/auth/token/', get_jwt_token, name='send_confirmation_code'),
    path('v1/users/me/', APIUser.as_view()),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignupView.as_view()),
]
