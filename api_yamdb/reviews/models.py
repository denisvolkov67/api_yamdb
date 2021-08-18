from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class UserRole:
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    CHOICES = [
        (ADMIN, "admin"),
        (MODERATOR, "moderator"),
        (USER, "user"),
    ]


class User(AbstractUser):
    bio = models.TextField(
        "Биография",
        blank=True,
    )
    role = models.CharField(
        verbose_name="Роль пользователя",
        max_length=16,
        choices=UserRole.CHOICES,
    )

    class Meta:
        ordering = ["username"]
        verbose_name = "User"
        verbose_name_plural = "Users"


class Categories(models.Model):
    name = models.CharField(verbose_name="Имя категории", max_length=256)
    slug = models.SlugField(verbose_name="Slug категории", unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(verbose_name="Имя жанра", max_length=256)
    slug = models.SlugField(verbose_name="Slug жанра", unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(verbose_name="Имя произведения")
    year = models.PositiveSmallIntegerField(
        verbose_name="Год создания произведения",
        validators=[
            MaxValueValidator(
                datetime.now().year,
                message="Ты умеешь перемещаться в будущее? Введи верную дату)",
            ),
            MinValueValidator(
                1,
                message="Введи корректную дату, дата не может быть ниже года",
            ),
        ],
    )
    description = models.TextField(verbose_name="Описание")
    genre = models.ManyToManyField(
        Genres, verbose_name="Жанр произведения", related_name="titles"
    )
    category = models.ForeignKey(
        Categories,
        verbose_name="Категория произведения",
        null=True,
        on_delete=models.SET_NULL,
        related_name="titles",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Title"
        verbose_name_plural = "Titles"

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_reviews"
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.CharField(max_length=500)
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
