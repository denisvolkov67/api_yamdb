from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Categories, Comments, Genres, Reviews, Title


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"
        read_only_fields = ("name",)


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = "__all__"
        read_only_fields = ("name",)


class TitleSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(read_only=True, many=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Title
        fields = "__all__"
        read_only_fields = ("genres", "category")


class ReviewsSerializer(serializers.Serializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Reviews
        fields = "__all__"
        read_only_fields = ("author", "average")

        validators = [
            UniqueTogetherValidator(
                queryset=Reviews.objects.all(),
                fields=("author", "title"),
            )
        ]


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comments
        fields = "__all__"
        read_only_fields = ("name", "author")

        validators = [
            UniqueTogetherValidator(
                queryset=Comments.objects.all(),
                fields=("review", "text", "author"),
            )
        ]
