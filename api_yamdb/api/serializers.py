from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import User, Review, Comments, Title, Category, Genre
from .validators import username_is_not_me, username_is_unique

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[username_is_unique]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[username_is_not_me, username_is_unique]
    )

    class Meta:
        model = User
        fields = ('email', 'username')


class CodeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        title = self.context.get('title')
        request = self.context.get('request')

        if (
            request.method != 'PATCH' and Review.objects.filter(
                title=title, author=request.user).exists()
        ):
            raise serializers.ValidationError(
                'Вы уже оценивали это произведение!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments


class CustomSerializerField(serializers.SlugRelatedField):

    def to_representation(self, value):
        return {'name': value.name, 'slug': value.slug}


class TitleReadSerializer(serializers.ModelSerializer):
    genre = CustomSerializerField(
        queryset=Genre.objects.all(),
        slug_field='slug', many=True
    )
    category = CustomSerializerField(
        queryset=Category.objects.all(), slug_field='slug')
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug')

    class Meta:
        fields = '__all__'
        model = Title
