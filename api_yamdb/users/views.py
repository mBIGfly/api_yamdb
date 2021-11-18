from api_yamdb.permissions import IsAdmin
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CodeSerializer, SignUpSerializer, UserSerializer

User = get_user_model()


class UserModelViewset(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=('get', 'patch'),
        detail=False, url_path='me', url_name='me',
        permission_classes=[
            permissions.IsAuthenticated,
        ]
    )
    def user_own_profile(self, request):
        user = request.user
        serializer = self.get_serializer(instance=user)
        if self.request.method == 'GET':
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        user = User.objects.create(
            email=email,
            username=username,
            is_active=False,
        )

        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            'Email confirmation',
            f'Your confirmation code: {confirmation_code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=True,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class CodeConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, *args, **kwargs):
        serializer = CodeSerializer(data=self.request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        username = serializer.validated_data.get('username')
        token = serializer.validated_data.get(
            'confirmation_code')

        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, token):
            return Response(
                'Wrong confirmation code!', status.HTTP_400_BAD_REQUEST
            )

        user.is_active = True
        user.save()
        token = RefreshToken.for_user(user)
        return Response(
            {'token': str(token.access_token)},
            status.HTTP_200_OK)
