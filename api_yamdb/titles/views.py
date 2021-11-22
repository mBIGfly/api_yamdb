from django.db.models import Avg

from api.permissions import IsAdminOrReadOnly
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleCreateSerializer, TitleSerializer)
from rest_framework import mixins, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .filters import TitleFilter
from .models import Category, Genre, Title


class RetrieveCreateDeleteViewSet(mixins.ListModelMixin,
                                  mixins.DestroyModelMixin,
                                  mixins.CreateModelMixin,
                                  GenericViewSet):
    pass


class CategoryViewSet(RetrieveCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    search_fields = ('name',)
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]


class GenreViewSet(RetrieveCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    search_fields = ('name',)
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]


class TitleViewSet(ModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = TitleSerializer
    filterset_fields = ('year',)
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    filterset_class = TitleFilter

    def get_serializer(self, *args, **kwargs):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer(*args, **kwargs)
        return self.serializer_class(*args, **kwargs)

    def get_queryset(self):
        return (
            Title.objects
            .prefetch_related('genre')
            .select_related('category')
            .annotate(rating_avg=Avg('reviews__score'))
        )
