from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


def username_is_not_me(value):
    if value == 'me':
        raise serializers.ValidationError(
            'You cannot use `me` as your username'
        )


def username_is_unique(value):
    if User.objects.filter(username=value).exists():
        raise serializers.ValidationError('This username already exists.')
