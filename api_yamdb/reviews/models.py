from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator




class Categories(models.Model):
    name = models.CharField(verbose_name='Имя категории',
                            max_length=256)
    slug = models.SlugField(verbose_name='Slug категории',
                            unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(verbose_name='Имя жанра',
                            max_length=256)
    slug = models.SlugField(verbose_name='Slug жанра',
                            unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(verbose_name='Имя произведения')
    year = models.IntegerField(
        verbose_name='Год создания произведения',
        validators=[
            MaxValueValidator(datetime.now().year,
                              message = 'Ты умеешь  перемещаться в будущее? Введи верную дату;)'),
            MinValueValidator(1, message = 'Введи корректную дату, дата не может быть ниже года')
        ]
    )
    description = models.TextField(verbose_name='Описание')
    genres = models.ManyToManyField(
        Genres,
        verbose_name='Жанр произведения',
        related_name='titles'
    )
    category = models.ForeignKey(
        Categories,
        verbose_name='Категория произведения',
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )


class UserRole():
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    CHOICES = [
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    ]

class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=16, 
        choices=UserRole.CHOICES,
    )
