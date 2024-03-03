from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """Модель пользователя"""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=20, verbose_name='номер телефона', **NULLABLE)
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=250, verbose_name='токен пользователя',
                                                **NULLABLE)

    def __str__(self):
        return f'{self.email} - {self.phone}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        permissions = [
            (
                'set_user_deactivate',
                'Can deactivate user'
            ),
            ('view_all_users',
             'просмотр всех пользователей'
             ),
        ]