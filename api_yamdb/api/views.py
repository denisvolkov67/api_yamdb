from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from reviews.models import Categories, Comments, Genres, Reviews, Title

from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CategoriesSerializer,
    CommentsSerializer,
    GenresSerializer,
    ReviewsSerializer,
    TitleSerializer,
)


class CategoriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ("name",)


class GenresViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ("name",)


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ("name",)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        new_queryset = Title.objects.filter(title=title)
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, review=title)

    def get_title_rating(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        title_sum_rating = sum(Reviews.objects.filter(title=title))
        title_count_rating = Reviews.objects.filter(title=title).count()
        avg_rating = title_sum_rating / title_count_rating
        return avg_rating


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        review = get_object_or_404(Reviews, pk=self.kwargs.get("reviews_id"))
        new_queryset = Comments.objects.filter(review=review)
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Reviews, pk=self.kwargs.get("reviews_id"))
        serializer.save(author=self.request.user, review=review)
