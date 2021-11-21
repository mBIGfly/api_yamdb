from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import my_year_validator


class User(AbstractUser):
    class UserRole:
        USER = 'user'
        ADMIN = 'admin'
        MODERATOR = 'moderator'
        choices = [
            ('user', 'user'),
            ('admin', 'admin'),
            ('moderator', 'moderator'),
        ]

    bio = models.TextField(
        verbose_name='user bio',
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name='user email',
        unique=True,
    )
    role = models.CharField(
        verbose_name='user role',
        max_length=25,
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def is_admin(self):
        return (
            self.role == self.UserRole.ADMIN
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == self.UserRole.MODERATOR


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Имя категории'
    )
    slug = models.CharField(
        max_length=50, unique=True,
        verbose_name='Адрес категории'
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id']

    def __str__(self):
        return self.name[:15]


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Имя жанра'
    )
    slug = models.CharField(
        max_length=50, unique=True,
        verbose_name='Адрес жанра'
    )

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['id']

    def __str__(self):
        return self.name[:15]


class Title(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        blank=True, null=True,
        validators=[my_year_validator],
    )
    description = models.CharField(
        max_length=200, blank=True, null=True,
        verbose_name='Короткое описание'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория произведения'
    )

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'
        ordering = ['id']

    def __str__(self):
        return self.name[:15]


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'Жанр:{self.genre} произведения {self.title}'


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Оцениваемое произведение'
    )
    text = models.CharField(
        max_length=200,
        verbose_name='Текст отзыва'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Время и дата публикации отзыва'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(0, message='Мин.Оценка 0'),
            MaxValueValidator(10, message='Макс.Оценка 10')
        ]
    )

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"],
                name="unique_review"
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'

    )
    text = models.CharField(
        max_length=200,
        verbose_name='Текст комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Время и дата публикации комментария'
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
