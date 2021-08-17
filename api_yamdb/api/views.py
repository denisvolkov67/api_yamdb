from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import (
    Categories,
    Comment,
    Genres,
    Review,
    Title,
    User,
    UserRole,
)
from django.db.models import Avg
from rest_framework.exceptions import ValidationError
from .filters import TitleFilter
from .permissions import IsAdmin, IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, ReviewsSerializer,
                          SignupSerializer, TitleSerializer,
                          TitleWriteSerializer, TokenSerializer,
                          UserSerializer)
from .utils import Util


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class RetrieveUpdateViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    pass


class BaseModelViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoriesViewSet(BaseModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ("name",)
    lookup_field = "slug"


class GenresViewSet(BaseModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (Title.objects.annotate(rating=Avg("reviews__score"))
                .order_by("name"))
    serializer_class = TitleSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializer
        return TitleWriteSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        if title.reviews.filter(author=self.request.user).exists():
            raise ValidationError(
                "Можно оставлять только одно ревью")
        serializer.save(author=self.request.user, title_id=title.id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        new_queryset = Comment.objects.filter(review=review)
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username", )
    lookup_field = "username"

    @action(methods=["get", "patch"], detail=False,
            permission_classes=(IsAuthenticated,), url_path="me")
    def me(self, request):
        if request.method == "GET":
            user = get_object_or_404(User, username=request.user.username)
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        if request.method == "PATCH":
            data = request.data
            if request.user.role == UserRole.USER:
                _mutable = data._mutable
                data._mutable = True
                data.update({"role": "user"})
                data._mutable = _mutable
            serializer = self.get_serializer(
                request.user, data=data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.update(request.user, data)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_200_OK, headers=headers
            )


class SignupViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        username = request.data.get("username")
        email = request.data.get("email")
        user = get_object_or_404(User, username=username)
        confirmation_code = default_token_generator.make_token(user)
        data = {
            "email_body": confirmation_code,
            "to_email": email,
            "email_subject": "confirmation_code",
        }
        Util.send_email(data)
        content = {"username": username, "email": email}
        return Response(content, status=status.HTTP_200_OK)


class TokenViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = TokenSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        confirmation_code = serializer.validated_data.get("confirmation_code")
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response(
                {"token": str(token)}, status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)
