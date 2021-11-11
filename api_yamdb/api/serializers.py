from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import User, Review, Comments, Title


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class CheckConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name',
                  'username', 'bio', 'email', 'role',)
        model = User


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


class TitleSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    # добавила поле для расчета рейтинга
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        fields = ('id', 'name', 'rating', 'author')
        model = Title
