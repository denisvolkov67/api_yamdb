from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Categories, Comments, Genres, Reviews, Title


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug')
        read_only_fields = ("name",)


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug')
        read_only_fields = ("name",)


class TitleSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True)
    category = CategoriesSerializer()
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('genre', 'category', 'rating')
        
        
class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(), slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Title
        
        
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
        read_only_fields = ("review", "author")

        validators = [
            UniqueTogetherValidator(
                queryset=Comments.objects.all(),
                fields=("review", "text", "author"),
            )
        ]
