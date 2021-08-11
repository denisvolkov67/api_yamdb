from enum import unique

from rest_framework.validators import UniqueValidator
from reviews.models import Categories, Genres, Title, User, UserRole
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
        read_only_fields = ('name',)


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'
        read_only_fields = ('name',)


class TitleSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(read_only=True, many=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('genres', 'category')


class AbstractUserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField('^[\w.@+-]', max_length=150)
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    role = serializers.ChoiceField(required=False, 
        choices=UserRole.CHOICES, 
        default=UserRole.USER)


class UserSerializer(AbstractUserSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)


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