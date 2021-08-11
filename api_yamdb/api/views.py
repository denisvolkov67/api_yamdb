from reviews.models import Categories, Genres, Title
from rest_framework import filters, viewsets, mixins
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitleSerializer,
                          TitleWriteSerializer)
from .filters import TitleFilter

class BaseModelViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    pass


class CategoriesViewSet(BaseModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', )
    lookup_field = 'slug'


class GenresViewSet(BaseModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializer
        return TitleWriteSerializer
