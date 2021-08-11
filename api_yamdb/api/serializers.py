from reviews.models import Categories, Genres, Title
from rest_framework import serializers


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug')


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
