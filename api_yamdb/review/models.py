from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


def validate_rate(value):
    if value not in [0, 10]:
        raise ValidationError('Оценка должна быть от 0 до 10!')


class Title(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review'
    )
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Comments(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Rating(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rating'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='rating'
    )
    score = models.IntegerField(validators=[validate_rate])

    def __str__(self):
        return self.score
