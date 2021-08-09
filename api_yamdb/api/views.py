from .models import Categories, Genres, Title
from rest_framework import filters, viewsets

from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitleSerializer)

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