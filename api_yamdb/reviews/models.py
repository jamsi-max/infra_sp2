import datetime
from django.contrib.auth import get_user_model
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                r"^[-a-zA-Z0-9_]+$",
                message="Slug может содержать латинские буквы, цифры и знак _",
            )
        ],
    )

    class Meta:
        verbose_name = "Жанры"
        verbose_name_plural = "Жанр"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                r"^[-a-zA-Z0-9_]+$",
                message="Slug может содержать латинские буквы, цифры и знак _",
            )
        ])

    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категория"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(datetime.date.today().year)
        ]
    )
    description = models.TextField()
    category = models.ForeignKey(
        Category, related_name="titles", null=True, on_delete=models.SET_NULL
    )
    genre = models.ManyToManyField(Genre, through="GenreTitle")

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Рейтинг",
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_review"
            )
        ]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
    )
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации", auto_now_add=True
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class GenreTitle(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL)
