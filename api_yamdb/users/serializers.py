from django.contrib.auth import get_user_model
from rest_framework import serializers

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
