
import math
import random
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response
from reviews.models import Categories, Genres, Title, User
from rest_framework import filters, mixins, viewsets, status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (CategoriesSerializer,
                          GenresSerializer, SignupSerializer,
                          TitleSerializer, TokenSerializer, UserSerializer)
from .utils import Util


class CreateViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    pass


class CategoriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', )


class GenresViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', )


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class SignupViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def perform_create(self, serializer):
        digits="0123456789"
        code=""
        for i in range(6):
            code+=digits[math.floor(random.random()*10)]
        data = {
            'email_body': code,
            'to_email': serializer.validated_data['email'],
            'email_subject': 'confirmation_code'
        }
        Util.send_email(data)

        serializer.save(confirmation_code=code)


class TokenView(CreateAPIView):
    serializer_class = TokenSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if user.confirmation_code == confirmation_code:
            refresh = RefreshToken.for_user(user)
        return Response({'token': refresh.access_token}, status=status.HTTP_200_OK)

class TokenViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = TokenSerializer

    def perform_create(self, serializer):
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)

        if user.confirmation_code == confirmation_code:
            refresh = RefreshToken.for_user(user)

            return Response({'token': refresh.access_token,}, status=status.HTTP_200_OK)

    