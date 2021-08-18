from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import (
    Categories,
    Comment,
    Genres,
    Review,
    Title,
    User,
    UserRole,
)
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ("name", "slug")


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ("name", "slug")


class TitleSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True)
    category = CategoriesSerializer()
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = "__all__"


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(), slug_field="slug", many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(), slug_field="slug"
    )

    class Meta:
        fields = "__all__"
        model = Title


class ReviewsSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.SlugRelatedField(read_only=True, slug_field="name")

    def validate(self, data):
        request = self.context["request"]
        title_id = self.context["view"].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if request.method == "POST":
            if Review.objects.filter(
                title=title, author=request.user
            ).exists():
                raise ValidationError
        return data

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ("title", "author")


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
        read_only_fields = ("review", "author")

        validators = [
            UniqueTogetherValidator(
                queryset=Comment.objects.all(),
                fields=("text", "author"),
            )
        ]


class AbstractUserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        r"^[\w.@+-]",
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    role = serializers.ChoiceField(
        required=False, choices=UserRole.CHOICES, default=UserRole.USER
    )


class UserSerializer(AbstractUserSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class SignupSerializer(AbstractUserSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "role",
        )
        read_only_fields = ("role",)

    def validate(self, attrs):
        if attrs["username"] == "me":

            raise serializers.ValidationError(
                "Нельзя использовать 'me' в качестве username!"
            )
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "username",
            "confirmation_code",
        )
