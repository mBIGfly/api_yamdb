from django.utils import timezone
from rest_framework import serializers


def my_year_validator(value):
    if value < 1900 or value > timezone.now().year:
        raise serializers.ValidationError(
            ('%(value)s is not a correcrt year!'),
            params={'value': value},
        )
