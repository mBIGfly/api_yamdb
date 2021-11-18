from django.contrib.auth.models import AbstractUser
from django.db import models


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
        verbose_name='user_bio',
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name='user_email',
        unique=True,
    )
    role = models.CharField(
        verbose_name='user_role',
        max_length=25,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    confirmation_code = models.CharField(
        max_length=6, default='000000')

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
