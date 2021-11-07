from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from review.models import Review, Comments, Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments


class TitleSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    rating = serializers.IntegerField(read_only=True, required=False) # добавила поле для расчета рейтинга

    class Meta:
        fields = ('id', 'name', 'rating', 'author')
        model = Title
