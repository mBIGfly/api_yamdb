from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrAdminOrModerator
from .serializers import (CategorySerializer, CodeSerializer,
                          CommentSerializer, GenreSerializer, ReviewSerializer,
                          SignUpSerializer, TitleCreateSerializer,
                          TitleReadSerializer, UserSerializer)
from reviews.models import Category, Genre, Review, Title, User

User = get_user_model()


class UserModelViewset(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True).order_by('id')
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    pagination_class = PageNumberPagination
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
        serializer.is_valid(raise_exception=True)
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


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    ordering = ['id']


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    pagination_class = PageNumberPagination


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrModerator,)
    pagination_class = PageNumberPagination

    def get_serializer_context(self):
        context = super(ReviewViewSet, self).get_serializer_context()
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        context.update({'title': title})
        return context

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        return title.reviews.all().order_by('id')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModerator,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_queryset = get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id')
        )
        return review_queryset.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    serializer_class = TitleReadSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleCreateSerializer
        return TitleReadSerializer
