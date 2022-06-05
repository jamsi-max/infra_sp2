import datetime as dt
import re

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                'Ошибка! Имя "me" использовать запрещено!'
            )
        return value


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ("username", "confirmation_code")


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Пользователь с таким именем уже существует.",
            )
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Пользователь с таким почтовым ящиком уже существует.",
            )
        ]
    )

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User

    def get_fields(self):
        fields = super(UserSerializer, self).get_fields()
        if (self.context["request"].user.is_user
                and self.context["request"].method == 'PATCH'):
            fields['role'] = serializers.ChoiceField(
                choices='user',
                read_only=True
            )
        return fields


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[
            UniqueValidator(
                queryset=Category.objects.all(),
                message="Такой slug уже существует",
            ),
            RegexValidator(
                re.compile(r"^[-a-zA-Z0-9_]+$"),
                message="Slug может содержать латинские буквы, цифры и знак _",
            ),
        ]
    )

    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        read_only_fields = fields


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )

    def validate_year(self, value):
        year = dt.date.today().year
        if not (0 < value <= year):
            raise serializers.ValidationError("Проверьте год произведения!")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    def validate(self, data):
        if self.context["request"].method != "POST":
            return data
        user = self.context["request"].user
        title_id = self.context["view"].kwargs["title_id"]
        if Review.objects.filter(author=user, title_id=title_id).exists():
            raise serializers.ValidationError("Нельзя оставить два отзыва!")
        return data

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="username"
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment
