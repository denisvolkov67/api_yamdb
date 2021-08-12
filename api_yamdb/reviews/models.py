from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Categories(models.Model):
    name = models.CharField(verbose_name="Имя категории", max_length=256)
    slug = models.SlugField(verbose_name="Slug категории", unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(verbose_name="Имя жанра", max_length=256)
    slug = models.SlugField(verbose_name="Slug жанра", unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(verbose_name="Имя произведения")
    year = models.IntegerField(
        verbose_name="Год создания произведения",
        validators=[
            MaxValueValidator(
                datetime.now().year,
                message="Ты умеешь  перемещаться в будущее? Введи верную дату;)",
            ),
            MinValueValidator(
                1,
                message="Введи корректную дату, дата не может быть ниже года",
            ),
        ],
    )
    description = models.TextField(verbose_name="Описание")
    genres = models.ManyToManyField(
        Genres, verbose_name="Жанр произведения", related_name="titles"
    )
    category = models.ForeignKey(
        Categories,
        verbose_name="Категория произведения",
        null=True,
        on_delete=models.SET_NULL,
        related_name="titles",
    )


class Reviews(models.Model):
    text = models.CharField(max_length=500)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )

    count = models.PositiveIntegerField(default=0)
    summ = models.PositiveIntegerField(default=0)
    average = models.PositiveIntegerField(default=0)
    Rating_CHOICES = (
        (1, "Poor"),
        (2, "Average"),
        (3, "Good"),
        (4, "Very Good"),
        (5, "Excellent"),
    )

    rating = models.IntegerField(choices=Rating_CHOICES, default=1)
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )



class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.CharField(max_length=500)
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )
