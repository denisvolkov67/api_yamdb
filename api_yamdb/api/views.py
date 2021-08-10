from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Categories, Genres, Title, User
from rest_framework import filters, mixins, serializers, viewsets

from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitleSerializer, UserSerializer)


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


