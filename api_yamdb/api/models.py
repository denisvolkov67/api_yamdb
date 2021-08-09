from datetime import datetime

from django.db import models


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
        verbose_name='Год создания произведения'
        
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
        on_delete=models.SET_NULL,
        related_name='titles'
        
    )