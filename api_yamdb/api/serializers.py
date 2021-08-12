from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import (Categories, Comments, Genres, Reviews, Title, User,
                            UserRole)


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


class AbstractUserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        '^[\w.@+-]',
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    role = serializers.ChoiceField(
        required=False,
        choices=UserRole.CHOICES,
        default=UserRole.USER
    )


class UserSerializer(AbstractUserSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)


class UserMeSerializer(AbstractUserSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',)


class SignupSerializer(AbstractUserSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'role',)
        read_only_fields = ('role',)

    def validate(self, attrs):
        if(attrs['username'] == 'me'):

            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве username!'
            )
        return attrs


class TokenSerializer(AbstractUserSerializer):
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)
